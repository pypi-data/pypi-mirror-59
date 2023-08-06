from django.test import TestCase, tag, override_settings
from unittest import skip

from aristotle_mdr.tests.utils import AristotleTestUtils
from aristotle_mdr import models
from aristotle_mdr.contrib.aristotle_pdf.downloader import PDFDownloader


@override_settings(ARISTOTLE_SETTINGS={
    'DOWNLOAD_OPTIONS': {'DOWNLOADERS': ['aristotle_mdr.contrib.aristotle_pdf.downloaders.PDFDownloader']}
})
class PDFDownloaderTestCase(AristotleTestUtils, TestCase):

    def setUp(self):
        super().setUp()
        self.item = models.ObjectClass.objects.create(
            name='Pokemon',
            definition='Pocket Monsters',
            submitter=self.editor
        )

    @tag('pdf')
    @skip('wkhtmltopdf not installed on travis')
    def test_pdf_download_generates_file(self):
        downloader = PDFDownloader([self.item.id], self.editor.id, {})
        fileobj = downloader.create_file()
        self.assertTrue(fileobj.size > 0)

    @tag('pdf_su')
    @skip('wkhtmltopdf not installed on travis')
    def test_pdf_download_generates_file_superuser(self):
        downloader = PDFDownloader([self.item.id], self.su.id, {})
        fileobj = downloader.create_file()
        self.assertTrue(fileobj.size > 0)
