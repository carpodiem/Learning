def resize_image(file_names):
    import subprocess, os
    result_dir = os.path.join(os.getcwd(), 'Result')
    if 'Result' not in os.listdir(os.getcwd()):
        os.mkdir(result_dir)
    for image in file_names:
        output_file = result_dir + '\\' + image.split('\\')[1] + '_res200.jpg'
        program_w_args = 'convert.exe ' + image + ' -resize 200 ' + output_file
        print(image.split('\\')[1])
        resize_it = subprocess.run(program_w_args)
        if resize_it.returncode == 0:
            print('Выполнено успешно!')
        else:
            print('Упс! Что-то пошло не так! Обретитесь к разработчкику.')

def list_of_files(source_dir):
    import glob, os.path
    image_files = glob.glob(os.path.join(source_dir, '*.jpg'))
    return image_files

# def image_threding(images):
#     import subprocess, os
#     result_dir = os.path.join(os.getcwd(), 'Result')
#     print(result_dir)
#     from multiprocessing import Pool
#     if __name__ == '__main__':
#         with Pool(processes = 2) as file_pool:
#             file_pool.map(resize_image, images)

images = list_of_files('Source')
resize_image(images)
# image_threding(images)