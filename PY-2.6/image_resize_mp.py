def resize_image(image):
    import os, subprocess
    result_dir = os.path.join(os.getcwd(), 'Result')
    file_name = image.split('\\')[1]
    output_file = result_dir + '\\' + file_name + '_res200.jpg'
    program_w_args = 'convert.exe ' + image + ' -resize 200 ' + output_file
    resize_it = subprocess.run(program_w_args)
    if resize_it.returncode == 0:
        print('Файл: ', file_name, ' - Выполнено успешно!')
    else:
        print('Файл: ', file_name, ' - Упс! Что-то пошло не так! Обретитесь к разработчкику.')

def list_of_files(source_dir):
    import glob, os.path
    image_files = glob.glob(os.path.join(source_dir, '*.jpg'))
    return image_files

def image_threding(images):
    import os
    from multiprocessing import Pool
    result_dir = os.path.join(os.getcwd(), 'Result')
    if 'Result' not in os.listdir(os.getcwd()):
        os.mkdir(result_dir)
    if __name__ == '__main__':
        with Pool(processes = 2) as file_pool:
            file_pool.map(resize_image, images)


images = list_of_files('Source')
image_threding(images)