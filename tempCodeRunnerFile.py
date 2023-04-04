num_processes = cpu_count()    
    # with Pool(num_processes) as w:
    #     #w=mp.Pool()
    #     w.starmap(menu.mpmenu,[(city_res_links[_],city_names[_]) for _ in range(len(city_res_links))])