import pandas
import os


def load_csv(file_path):
    # first check that file exists
    if not os.path.exists(file_path):
        return None

    # now load into dataframe
    temp_dataframe = pandas.read_csv(file_path)

    # format data and return
    return_dataframe = pandas.DataFrame()
    if 'login' in temp_dataframe and 'start_date' in temp_dataframe and 'era' in temp_dataframe:
        return_dataframe['login'] = temp_dataframe['login']
        return_dataframe['start_date'] = temp_dataframe['start_date']
        return_dataframe['era'] = temp_dataframe['era']
        return return_dataframe
    else:
        return None


if __name__ == '__main__':
    # Runs analysis for RQ1 on all data csv files in 1st degree child folder (does not search past immediate child)
    # search current directory for 'data' folder and get all files inside
    directory_list = os.listdir()
    if 'data' not in directory_list:
        print('Data folder not found!')
        exit(0)


    # filter out any non-csv files from list of files in data folder
    files_list = os.listdir('data')
    data_files_list = [file for file in files_list if '.csv' in file]


    # load each file into master dataframe
    master_dataframe = pandas.DataFrame()
    for file in data_files_list:
        # create file path
        file_path = './data/' + file

        # load data
        load_dataframe = load_csv(file_path)

        # merge into master dataframe
        if load_dataframe is not None:
            # add file_name column for the repo the data was taken from
            load_dataframe['file_name'] = file.replace('.csv', '')
            master_dataframe = pandas.concat([master_dataframe, load_dataframe], ignore_index=True)

    # save merged data to csv
    master_dataframe.to_csv('merged_data.csv')
