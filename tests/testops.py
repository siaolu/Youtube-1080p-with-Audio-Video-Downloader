import unittest
from unittest.mock import patch, mock_open
import utils
import media_downloads

class TestUtils(unittest.TestCase):
    def test_load_config(self):
        """ Test loading configuration from a file. """
        with patch('builtins.open', mock_open(read_data='{"debug": true, "port": 5000}')) as mocked_file:
            config = utils.load_config('dummy_path.json')
            self.assertEqual(config['debug'], True)
            self.assertEqual(config['port'], 5000)
            mocked_file.assert_called_once_with('dummy_path.json', 'r')

    def test_safe_file_operation_fail(self):
        """ Test the safe file operation decorator handling an exception. """
        @utils.safe_file_operation
        def faulty_function(path):
            raise Exception("Intentional Failure")

        with self.assertRaises(Exception) as context:
            faulty_function('/fake/path')

        self.assertTrue('Intentional Failure' in str(context.exception))

    def test_read_write_file(self):
        """ Test read and write file utility functions. """
        test_data = "Hello, world!"
        with patch('builtins.open', mock_open(read_data=test_data)) as mocked_file:
            # Testing write operation
            utils.write_to_file('dummy_path.txt', test_data)
            mocked_file().write.assert_called_once_with(test_data)

            # Testing read operation
            read_data = utils.read_from_file('dummy_path.txt')
            self.assertEqual(read_data, test_data)
            mocked_file.assert_called_with('dummy_path.txt', 'r')

class TestMediaDownloads(unittest.TestCase):
    def test_download_video(self):
        """ Test the video download functionality. """
        with patch('media_downloads.YouTube') as mocked_youtube:
            mocked_youtube.return_value.streams.filter.return_value.order_by.return_value.desc.return_value.first.return_value.download.return_value = 'path/to/video.mp4'
            result = media_downloads.download_video('http://youtube.com/fakevideo', '/downloads')
            self.assertEqual(result, 'path/to/video.mp4')

    def test_extract_audio(self):
        """ Test audio extraction from video. """
        with patch('media_downloads.mpe.VideoFileClip') as mocked_clip:
            mocked_clip.return_value.audio.write_audiofile.return_value = True
            result = media_downloads.extract_audio('path/to/video.mp4', '/path/to/audio.mp3')
            self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
