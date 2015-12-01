# Test export module
import os
import flopy

pth = os.path.join('..', 'examples', 'data', 'mf2005_test')
namfiles = [namfile for namfile in os.listdir(pth) if namfile.endswith('.nam')]


def export_netcdf(namfile):
    print(namfile)
    m = flopy.modflow.Modflow.load(namfile, model_ws=pth, verbose=False)
    if m.dis.lenuni == 0:
        print('skipping...lenuni==0 (undefined)')
        return
    if m.dis.botm.shape[0] != m.nlay:
        print('skipping...botm.shape[0] != nlay')
        return
    assert m, 'Could not load namefile {}'.format(namfile)
    assert isinstance(m, flopy.modflow.Modflow)

    # Do not fail if netCDF4 not installed
    try:
        import netCDF4
    except:
        return

    try:
        fnc = m.export(os.path.join('temp', m.name + '.nc'))
        fnc.write()
    except Exception as e:
        print('fail:\n  ' + str(e))
    return


def test_netcdf():
    for namfile in namfiles:
        yield export_netcdf, namfile
    return

if __name__ == '__main__':
    for namfile in namfiles:
        export_netcdf(namfile)