import pandas as pd

def write_relative_sharpness_to_csv(mtf50_rel, mtf10_rel, output_fname):
    mtf50_rel = mtf50_rel.copy()
    mtf10_rel = mtf10_rel.copy()
    mtf50_rel['%MTF cutoff'] = 50
    mtf10_rel['%MTF cutoff'] = 10
    pd.concat((mtf50_rel, mtf10_rel), axis=0).to_csv(output_fname)
    print(f'File saved: {output_fname}')

def load_csv(csv_fname):
    df = pd.read_csv(csv_fname)
    mtf50_rel = df[df['%MTF cutoff'] == 50]
    mtf10_rel = df[df['%MTF cutoff'] == 10]
    return mtf50_rel, mtf10_rel