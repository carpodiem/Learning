import subprocess, os, glob
def resize_image(file_names):
    result_dir = os.path.join(os.getcwd(), 'Result')
    if 'Result' not in os.listdir(os.getcwd()):
        os.mkdir(result_dir)
    for image in file_names:
        output_file = os.path.join(result_dir, os.path.basename(os.path.splitext(image)[0]) + '_res200.jpg')
        program_args = os.path.join(os.path.join(os.getcwd(),image + ' -resize 200 ' + output_file))
        program_w_args = os.path.join(os.getcwd(), 'convert.exe ' + program_args)
        resize_it = subprocess.run(program_w_args)
        print(os.path.basename(image))
        if resize_it.returncode == 0:
            print('Выполнено успешно!')
        else:
            print('Упс! Что-то пошло не так! Обретитесь к разработчкику.')

def list_of_files(source_dir):
    image_files = glob.glob(os.path.join(source_dir, '*.jpg'))
    return image_files

images = list_of_files('Source')
resize_image(images)