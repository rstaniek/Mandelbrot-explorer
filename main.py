from tkinter import *
from mandelbrot import Coordinates, Mandelbrot
from guiconfig import AppConfig
import time, subprocess, os, platform
import numpy as np

fields = ('X offset', 'Y offset', 'Zoom level', 'Image Height', 'Image Width')
x_s = 'X offset'
y_s = 'Y offset'
z_s = 'Zoom level'
h_s = 'Image Height'
w_s = 'Image Width'
it_s = 'Iterations'
gmm_s = 'Gamma'
col_s = 'Color map'

program = Mandelbrot()
config = AppConfig()

scale = None
gamma_scale = None
color_option = None

currentcolor_var = None
postrenderselect_var = None
showborder_var = None

def makeform(root, f):
    entries = {}
    for field in f:
        row = Frame(root)
        lbl = Label(row, width=20, text=field+': ', anchor='w')
        ent = Entry(row)
        ent.insert(0, '0.0')
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lbl.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        entries[field] = ent
    return entries

def makeiterscale(root):
    row = Frame(root)
    lbl_scale = Label(row, width=20, text=it_s+': ', anchor='w')
    scale = Scale(row, from_=min(config.iter_steps), to=max(config.iter_steps), orient=HORIZONTAL, command=iter_scale_valuecheck)
    row.pack(side=TOP, fill=X, padx=5, pady=5)
    lbl_scale.pack(side=LEFT)
    scale.pack(side=RIGHT, expand=YES, fill=X)
    return scale

def iter_scale_valuecheck(value):
    new_val = min(config.iter_steps, key=lambda x: abs(x - float(value)))
    scale.set(new_val)

def makegammascale(root):
    row = Frame(root)
    lbl_gamma = Label(row, width=20, text=gmm_s+': ', anchor='w')
    gamma_scale = Scale(row, from_=0, to=10, orient=HORIZONTAL)
    row.pack(side=TOP, fill=X, padx=5, pady=5)
    lbl_gamma.pack(side=LEFT)
    gamma_scale.pack(side=RIGHT, expand=YES, fill=X)
    gamma_scale.set(int(np.multiply(config.image['gamma'], 10)))
    return gamma_scale

def makecoloroptionmenu(root):
    row = Frame(root)
    lbl_col = Label(row, width=20, text=col_s+': ', anchor='w')
    color_option = OptionMenu(row, currentcolor_var, *config.cmaps)
    row.pack(side=TOP, fill=X, padx=5, pady=5)
    lbl_col.pack(side=LEFT)
    color_option.pack(side=RIGHT, expand=YES, fill=X)
    return color_option

def makeBorderCheckbox(root):
    row = Frame(root)
    border_check = Checkbutton(row, text='Border enabled', variable=showborder_var, onvalue=True, offvalue=False)
    border_check.pack(side=LEFT)
    row.pack(side=TOP, expand=YES, fill=X)

def makesaveselectmenu(root):
    labelframe = LabelFrame(root, text='Post render step selection')
    save_radio = Radiobutton(labelframe, text='Save as PNG', value=1, variable=postrenderselect_var)
    show_radio = Radiobutton(labelframe, text='Show figure', value=2, variable=postrenderselect_var)
    labelframe.pack(side=TOP, fill=X, padx=5, pady=5)
    save_radio.pack(side=LEFT)
    show_radio.pack(side=LEFT)

def init_fields(ents):
    ents[x_s].delete(0, END)
    ents[y_s].delete(0, END)
    ents[z_s].delete(0, END)
    ents[h_s].delete(0, END)
    ents[w_s].delete(0, END)
    ents[x_s].insert(0, config.coordinates['x'])
    ents[y_s].insert(0, config.coordinates['y'])
    ents[z_s].insert(0, config.coordinates['zoom'])
    ents[h_s].insert(0, config.image['size']['height'])
    ents[w_s].insert(0, config.image['size']['width'])
    return ents

def save_coordinates(x,y,z):
    cfg = {}
    cfg['x'] = x
    cfg['y'] = y
    cfg['zoom'] = z
    config.update_config(coordinates=cfg)

def save_imgdata(cmap, gamma, img_h, img_w):
    cfg = {}
    cfg['gamma'] = gamma
    cfg['cmap'] = cmap
    cfg['size'] = {'height': img_h, 'width': img_w}
    config.update_config(image=cfg)

def run_calculation(data, iters, gamma, cmap, sb):
    program.close_all_figs()
    x_f = float(data[x_s].get())
    y_f = float(data[y_s].get())
    z_f = float(data[z_s].get())
    h_i = int(data[h_s].get())
    w_i = int(data[w_s].get())
    it_i = int(iters.get())
    cmp_s = str(cmap.get())
    gmm_f = np.divide(float(gamma.get()), 10.0)
    save_coordinates(x_f, y_f, z_f)
    save_imgdata(cmp_s, gmm_f, h_i, w_i)
    print('Starting Mandelbrodt set calculation with following params:\n\tx-offset:\t{}\n\ty-offset:\t{}\n\tzoom:\t\t{}:1\n\tmax-iterations:\t{}\n\tgamma:\t\t{}\n\tcmap:\t\t{}\n\timage-height:\t{}\n\timage-width:\t{}\n'
        .format(x_f, y_f, z_f, it_i, gmm_f, cmp_s, h_i, w_i))
    start = time.process_time()
    coords = Coordinates.from_values(x_f, y_f, z_f)
    program.mandelbrot_coord(coords, maxiter=it_i, gamma=gmm_f, cmap=cmp_s, height=h_i, width=w_i, showborder=sb.get())
    end = time.process_time()
    print('Calculation complete. Elapsed: {}s'.format(end - start))
    if postrenderselect_var.get() == 1:
        save_calc()
    else:
        program.showfig()

def save_calc():
    print('Saving image...')
    file = program.save_visualization()
    print('Image saved!')
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    print(path)
    if platform.system() == 'Windows':
        subprocess.Popen(r'explorer /select,"%s"' % path)  
    else:
        print('Not supported in this OS! Open it yourself.')

if __name__ == '__main__':
    loacl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), r"images")
    root = Tk()
    config.get_config()
    ents = makeform(root, fields)
    ents = init_fields(ents)
    scale = makeiterscale(root)
    gamma_scale = makegammascale(root)
    #border_checkbox = makeBorderCheckbox(root)
    currentcolor_var = StringVar(root)
    currentcolor_var.set(config.image['cmap'])
    color_option = makecoloroptionmenu(root)
    postrenderselect_var = IntVar(root)
    makesaveselectmenu(root)
    postrenderselect_var.set(2)
    showborder_var = BooleanVar(root)
    makeBorderCheckbox(root)
    showborder_var.set(True)

    def onReturn(e):
        (lambda e=ents, it=scale, gm=gamma_scale, c=currentcolor_var, sb=showborder_var: run_calculation(e, it, gm, c, sb))

    root.bind('<Return>', onReturn)
    
    btn_run = Button(root, text='Run', command=(lambda e=ents, it=scale, gm=gamma_scale, c=currentcolor_var, sb=showborder_var: run_calculation(e, it, gm, c, sb)))
    btn_run.pack(side=LEFT, padx=5, pady=5)
    # btn_save = Button(root, text='Save Visualization', command=save_calc)
    # btn_save.pack(side=LEFT, padx=5, pady=5)
    btn_show = Button(root, text='Show folder', command=(lambda : subprocess.Popen(r'explorer "%s"' % loacl_path)) if platform.system() == 'Windows' else print('Not supported in this OS! Open it yourself.'))
    btn_show.pack(side=LEFT, padx=5, pady=5)

    row = Frame(root)
    row.pack(side=TOP, fill=X, padx=5, pady=5)
    btn_exportcfg = Button(row, text='Export config', command=(lambda: config.export_config()))
    btn_exportcfg.pack(side=LEFT)
    root.mainloop()