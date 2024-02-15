import os


class Folder:

    folder_path = "C:/Users/tusha/Desktop/vscode/SWIGGY"

    def get_folder(self):
        current_folder_path = self.folder_path

        return current_folder_path

    def get_file(self, str):
        fold_path = self.get_folder()

        return f'{fold_path}/{str}.csv'

    def getdbfolder(self, Cname):
        current_path = self.get_folder()
        med_path = '/txt_files/'
        target_path = f'{Cname}'
        med = current_path + med_path

        if not os.path.exists(med):
            os.makedirs(med)
        fold_path = med + target_path

        if not os.path.exists(fold_path):
            os.makedirs(fold_path)

        return fold_path

    def getdbfile(self, stng, Cname):
        fold_path = self.getdbfolder(Cname)

        if (stng == "det_links"):
            return f'{fold_path}/restaurant_det_links_{Cname}.csv'

        if (stng == "tot"):
            return f'{fold_path}/total_restaurants_{Cname}.csv'

    def getmenufolder(self, Cname):
        current_path = self.get_folder()
        med_path = f'/txt_files/{Cname}'
        target_path = '/menus'
        med = current_path + med_path

        if not os.path.exists(med):
            os.makedirs(med)
        fold_path = med + target_path

        if not os.path.exists(fold_path):
            os.makedirs(fold_path)
        return fold_path

    def getmenudb(self, Cname, resname):
        fold_path = self.getmenufolder(Cname)
        target_path = f'/restaurant_{resname}.csv'
        fpath = fold_path + target_path
        return fpath


class Multi_res_links:
    '''This class is to take restaurant_links{citynames}
    from different folders and output them as an array'''

    def get_links(self, flist):
        '''This function takes citynames list as a parameter and outputs a 2-D array'''
        rlinks = []
        fp = Folder()
        for name in flist:
            clinks = []
            file1 = fp.getdbfile("det_links", name)
            with open(file1, 'r', encoding='utf-8') as file:
                lines = file.readlines()[1:]

                for line in lines:
                    lind = line.rfind(',')
                    link = line[lind+1:]
                    clinks.append(link.strip())
            if len(clinks) <= 112:
                rlinks.append(clinks)
            else:
                rlinks.append(clinks[:112])

        return rlinks
