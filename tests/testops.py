import unittest
from unittest.mock import patch, MagicMock

from media_downloads import download_video, download_audio, convert_to_mp3, download_and_combine


class TestDownloadOperations(unittest.TestCase):
    """
    Contains unit tests for the media download functions. Tests video, audio, and
    combination download functionality using mocked objects.
    """

    def setUp(self):
        """
        Prepares the test fixture, setting up a mock YouTube object and its expected
        behaviors for streams and downloads.
        """
        self.mock_yt = MagicMock()
        self.mock_yt.streams.filter.return_value.first.return_value = MagicMock(
            filesize=1024, download=MagicMock(), title="ExampleVideo"
        )
        self.mock_folder_name = "test_folder"

    @patch('media_downloads.slugify')
    @patch('media_downloads.FileMetadata')
    def test_download_video(self, mock_metadata, mock_slugify):
        """
        Ensures that the download_video function processes downloads correctly
        and handles file metadata properly.
        """
        mock_slugify.return_value = "examplevideo"
        mock_metadata.return_value = MagicMock(filename="examplevideo.mp4")

        result = download_video(self.mock_yt, self.mock_folder_name)
        self.assertIn("Downloaded", result[0])

    @patch('media_downloads.slugify')
    @patch('media_downloads.FileMetadata')
    def test_download_audio(self, mock_metadata, mock_slugify):
        """
        Checks that download_audio downloads and converts audio correctly,
        including calling the convert_to_mp3 function.
        """
        self.mock_yt.streams.filter.return_value.desc.return_value.first.return_value = MagicMock(
            filesize=512, download=MagicMock(), title="ExampleAudio"
        )
        mock_slugify.return_value = "exampleaudio"
        mock_metadata.return_value = MagicMock(filename="exampleaudio.webm")

        with patch('media_downloads.convert_to_mp3') as mock_convert:
            result = download_audio(self.mock_yt, self.mock_folder_name)
            mock_convert.assert_called_once()
            self.assertIn("Downloaded and converted", result[0])

    @patch('os.remove')
    @patch('moviepy.editor.AudioFileClip')
    def test_convert_to_mp3(self, mock_audio_clip, mock_remove):
        """
        Verifies that convert_to_mp3 function converts audio files to mp3 format
        and performs necessary file operations like deletion of the original.
        """
        mock_clip_instance = MagicMock()
        mock_audio_clip.return_value = mock_clip_instance

        convert_to_mp3(self.mock_folder_name, "exampleaudio")

        mock_audio_clip.assert_called_once_with(self.mock_folder_name + "/exampleaudio.webm")
        mock_clip_instance.write_audiofile.assert_called_once()
        mock_remove.assert_called_once()

    @patch('media_downloads.download_video')
    @patch('media_downloads.download_audio')
    def test_download_and_combine(self, mock_download_audio, mock_download_video):
        """
        Ensures that download_and_combine coordinates the downloading and combining
        of video and audio into a single file effectively.
        """
        mock_download_video.return_value = ("Video downloaded", "green")
        mock_download_audio.return_value = ("Audio downloaded and converted", "green")

        result = download_and_combine(self.mock_yt, self.mock_folder_name)
        self.assertIn("combined with audio", result[0])


if __name__ == '__main__':
    unittest.main()
