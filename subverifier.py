# taken from bottom of CSE158 assignment 2 document
import unittest
import os
import magic
import requests


def test_workbook(path):
	f = open("workbook.html", 'r')
	t = f.read()
	if not t.startswith('<!DOCTYPE html>'):
		print("Your workbook submission is not a html file (does not start with '<!DOCTYPE html>')")
		print("Please save your work as html (e.g. do not just change the extension)")
		raise Exception
	f.close()


def test_video(url):
	if 'youtube' in url or 'youtu.be' in url:
		print("Looks like your video is a youtube link (" + url + ")")
		print("No further tests will be run on your file: please make sure it is publicly viewable")
		return

	FILE_ID = None
	if "id=" in url:
		FILE_ID = url.split("id=")[1].split('/')[0]
	elif '/d/' in url:
		FILE_ID = url.split("/d/")[1].split('/')[0]

	if FILE_ID is None:
		print("Couldn't determine file ID; expected a url of the form https://drive.google.com/file/d/FILE_ID/view?usp=drive_link or https://drive.google.com/uc?export=download&id=FILE_ID")
		print('(got """' + url + '""")')
		raise Exception

	print("Looks like your google drive file ID is " + FILE_ID)

	url_fixed = "https://drive.google.com/uc?export=download&id=" + FILE_ID
	r = requests.get(url_fixed, stream=True)
	print("Trying to download from " + url_fixed)

	chunk = next(r.iter_content(chunk_size=1024 * 1024))
	if len(chunk) < 1024 * 1024:
		chunk = chunk.decode('utf8')
		if "Virus scan warning" in chunk:
			print("Looks like your file is too large for Google to scan for viruses")
			uuid = chunk.split('uuid" value="')[1].split('"')[0]
			url_fixed = (
				"https://drive.usercontent.google.com/download?id=" + FILE_ID
				+ "&export=download&confirm=t&uuid=" + uuid
			)
			print("Trying to download from " + url_fixed)
			r = requests.get(url_fixed, stream=True)
			chunk = next(r.iter_content(chunk_size=1024 * 1024))
		else:
			print("Looks like your video file is less than 1mb; it is probably not a video")
			raise Exception

	print("Confirmed that your video file is greater than 1mb; checking file type")
	mime = magic.Magic(mime=True)
	typename = mime.from_buffer(chunk)
	if not "video/mp4" in typename:
		print("Your file is not an mp4 video file (type=" + typename + ")")
		raise Exception

	print("Everything looks okay! On your own, please verify that you can download a working video using the assignment script in the spec")
	# print("wget -O output.mp4 '" + url_fixed + "'")


class TestFiles(unittest.TestCase):
	@weight(0)
	def test_submitted_files(self):
		"""Check submitted files"""
		missing_files = check_submitted_files(['workbook.html', 'video_url.txt'])
		for path in missing_files:
			print('Missing {0}'.format(path))
		self.assertEqual(len(missing_files), 0, 'Missing some required files!')
		print('All required files submitted!')
		test_workbook("workbook.html")
		f = open("video_url.txt", 'r')
		url = f.read().strip()
		test_video(url)
		f.close()