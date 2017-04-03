import os
import subprocess
import glob
from multiprocessing import Pool


def resize_image(image):
    result_dir = os.path.join(os.getcwd(), 'Result')
    output_file = os.path.join(result_dir, os.path.basename(os.path.splitext(image)[0]) + '_res200.jpg')
    program_args = os.path.join(os.path.join(os.getcwd(), image + ' -resize 200 ' + output_file))
    program_w_args = os.path.join(os.getcwd(), 'convert.exe ' + program_args)
    file_name = os.path.basename(image)
    resize_it = subprocess.run(program_w_args)
    if resize_it.returncode == 0:
        print('Файл: ', file_name, ' - Выполнено успешно!')
    else:
        print('Файл: ', file_name, ' - Упс! Что-то пошло не так! Обретитесь к разработчкику.')


def list_of_files(source_dir):
    image_files = glob.glob(os.path.join(source_dir, '*.jpg'))
    return image_files


def image_threding(images):
    result_dir = os.path.join(os.getcwd(), 'Result')
    if 'Result' not in os.listdir(os.getcwd()):
        os.mkdir(result_dir)
    if __name__ == '__main__':
        with Pool(processes=2) as file_pool:
            file_pool.map(resize_image, images)


images = list_of_files('Source')
image_threding(images)
