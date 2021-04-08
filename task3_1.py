#
#    --help - вывести справочное сообщение;
#    -s | --src-dir - исходная директория, по умолчанию ".";
#    -d | --dst-dir - целевая директория, по умолчанию ".".

import os
import click
import eyed3

@click.command()
@click.option('-s', '--src-dir',
			  type=click.Path(),
			  help='Source directory.',
			  default=os.getcwd())
@click.option('-d', '--dst-dir',
			  type=click.Path(),
			  help='Destination directory.',
			  default=os.getcwd())
def main(src_dir, dst_dir):

	"""Sort this shit!"""

	source_path_exists = os.path.exists(src_dir)
	if source_path_exists:
		files_list = get_files_list(src_dir)
		if files_list:
			for file_name in files_list:
				file_handler(dst_dir, src_dir, file_name)
			print('Done')
		else:
			print('ERROR: There are no *.mp3 files')
	else:
		print('ERROR: No such directory')

def file_handler(destination_dir, source_dir, file_name):
	artist, title, album = get_file_tags(os.path.join(source_dir, file_name))
	if artist == None or album == None:
		pass
	else:
		new_file_name = file_name
		if title != None:
			new_file_name = f'{title} - {artist} - {album}.mp3'
		destination_path = os.path.join(destination_dir, artist, album)
		destination_dir_maked = make_dest_dir(destination_path)
		if destination_dir_maked:
			result = move_file(source_dir, destination_path, file_name, \
							   new_file_name)
			if not result:
				print(f'ERROR: It is not possible to move the {file_name} file')
		else:
			print('ERROR: Unable to create path, no permissions, \
			       check this and try again')
def move_file(source_path, destination_path, file_name, new_file_name):
	path_from = os.path.join(source_path, file_name)
	path_to = os.path.join(destination_path, new_file_name)
	try:
		if os.path.isfile(path_to):
			os.remove(path_to)
		os.rename(path_from, path_to)
	except:
		return False
	else:
		show_info(path_from, path_to)
		return True

def show_info(path_from, path_to):
	path_from = path_from.replace(os.getcwd(), '')
	path_to = path_to.replace(os.getcwd(), '')
	print(f'{path_from} > {path_to}')

def make_dest_dir(destination_path):
	destination_path_exists = os.path.exists(destination_path)
	if destination_path_exists:
		write_permission = os.access(destination_path, mode=os.W_OK)
		if not write_permission:
			return False
	else:
		try:
			os.makedirs(destination_path, mode=0o777, exist_ok=True)
		except:
			return False
	return True
def get_file_tags(file_name):
	mp3_file = eyed3.load(file_name)
	try:
		tags = [mp3_file.tag.artist, mp3_file.tag.title, mp3_file.tag.album]
	except AttributeError:
		tags = [None, None, None]
	for i, tag in enumerate(tags):
		if tag != None:
			tags[i] = tag.strip()
	return tags
def get_files_list(directory):
	files = os.listdir(directory)
	return list(filter(lambda x: x.endswith('.mp3'), files))

if __name__ == '__main__':
	main()
