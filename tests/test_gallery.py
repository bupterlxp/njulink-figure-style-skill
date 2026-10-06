"""Behavioural checks for gallery ingestion and user-edit preservation."""
from contextlib import redirect_stdout
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import cards
import build_index
import ingest
from contact_sheet import fit, grid


class GalleryBehaviour(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.public = self.root / "gallery"
        self.local = self.root / "gallery-local"
        self.inputs = self.root / "inputs"
        for directory in (self.public, self.local, self.inputs):
            directory.mkdir()
        self.override = patch.multiple(cards, ROOT=self.root, GALLERIES=[self.public, self.local])
        self.override.start()
        self.addCleanup(self.override.stop)

    def picture(self, name, colour="#57BDB5", size=(400, 300)):
        path = self.inputs / name
        image = Image.new("RGB", size, "white")
        draw = ImageDraw.Draw(image)
        w, h = size
        draw.rectangle((w//6, h//6, w//2, 5*h//6), fill=colour)
        draw.rectangle((2*w//3, h//3, 5*w//6, 5*h//6), fill=colour)
        image.save(path)
        return path

    def test_similar_private_image_is_kept_and_public_card_unchanged(self):
        source = self.picture("public.png")
        ingest.register(source, self.public, dedup=False, source="public")
        card = self.public / "public.md"
        meta, body = cards.read(card)
        meta["edited"] = True
        cards.write(card, meta, "User-corrected interpretation")
        before = card.read_bytes()
        # Same chart layout and a new palette must not be silently discarded.
        variant = self.picture("private.png", colour="#B6A4D8")
        status, ident, similar = ingest.register(variant, self.local)
        self.assertEqual(status, "added")
        self.assertTrue((self.local / f"{ident}.png").exists())
        self.assertIsNotNone(similar)
        self.assertEqual(card.read_bytes(), before)

    def test_pixel_duplicate_and_resized_source_are_skipped(self):
        source = self.picture("large.png", size=(2300, 1600))
        ingest.register(source, self.local, dedup=False)
        copy = self.inputs / "renamed.png"
        copy.write_bytes(source.read_bytes())
        status, _, _ = ingest.register(copy, self.local)
        self.assertEqual(status, "duplicate")
        self.assertEqual(len(cards.images(self.local)), 1)
        with Image.open(self.local / "large.png") as image:
            self.assertEqual(max(image.size), 2000)

    def test_same_name_different_data_is_not_overwritten(self):
        source = self.picture("result.png")
        ingest.register(source, self.local, dedup=False)
        before = (self.local / "result.png").read_bytes()
        source = self.picture("result.png", colour="#E5A1AF")
        status, ident, _ = ingest.register(source, self.local)
        self.assertEqual((status, ident), ("added", "result-2"))
        self.assertEqual((self.local / "result.png").read_bytes(), before)

    def test_user_edited_card_survives_write_and_prune(self):
        card = self.local / "notes.md"
        cards.write(card, {"title": "Keep", "edited": True}, "Human content")
        with self.assertRaises(ValueError):
            cards.write(card, {"title": "Replace"}, "Generated content")
        with redirect_stdout(io.StringIO()):
            build_index.build(self.local, prune=True)
        self.assertEqual(cards.read(card)[1].strip(), "Human content")

    def test_updated_image_does_not_trust_stale_source_digest(self):
        source = self.picture("original.png")
        ingest.register(source, self.local, dedup=False)
        original = source.read_bytes()
        replacement = self.picture("changed.png", colour="#E5A1AF")
        (self.local / "original.png").write_bytes(replacement.read_bytes())
        candidate = self.inputs / "candidate.png"
        candidate.write_bytes(original)
        status, _, _ = ingest.register(candidate, self.local)
        self.assertEqual(status, "added")

    def test_ambiguous_id_needs_path(self):
        for directory in (self.public, self.local):
            Image.new("RGB", (10, 10), "white").save(directory / "same.png")
        with self.assertRaises(ValueError):
            cards.find("same")
        self.assertEqual(cards.find(self.local / "same.png"), self.local / "same.png")

    def test_transparency_composites_on_white_and_compare_renders(self):
        source = self.inputs / "transparent.png"
        Image.new("RGBA", (20, 10), (0, 0, 0, 0)).save(source)
        image = fit(source, 200, 200)
        self.assertEqual(image.getpixel((0, 0)), (255, 255, 255))
        out = self.root / "compare.png"
        with redirect_stdout(io.StringIO()):
            grid([(source, "A", "Reference"), (source, "B", "Result")], out, 240, 2)
        with Image.open(out) as result:
            self.assertGreater(result.width, 480)
            self.assertGreater(result.height, 10)


if __name__ == "__main__":
    unittest.main()
