import os
import sys
import pytest

from igdiscover.__main__ import main
from .utils import datapath, resultpath, files_equal


@pytest.fixture
def run(tmpdir):
    def _run(args, expected):
        """
        Run IgDiscover, redirecting stdout to a temporary file.
        Then compare the output with the contents of an expected file.
        """
        outpath = str(tmpdir.join('output'))
        print('Running:', ' '.join(args))
        with open(outpath, 'w') as f:
            old_stdout = sys.stdout
            sys.stdout = f
            main(args)
            sys.stdout = old_stdout
        assert files_equal(expected, outpath)

    return _run


def test_main():
    with pytest.raises(SystemExit) as exc:
        main(['--version'])
    assert exc.value.code == 0


def test_group_by_barcode_only(run):
    args = ['group', '-b', '4', datapath('ungrouped.fasta')]
    run(args,  resultpath('grouped-by-barcode-only.fasta'))


def test_group_by_pseudo_cdr3(run):
    args = ['group', '-b', '4', '--pseudo-cdr3=-5:-2', '--trim-g', datapath('ungrouped.fasta')]
    run(args,  resultpath('grouped.fasta'))


def test_group_by_pseudo_cdr3_barcode_at_end(run):
    args = ['group', '-b', '-4', '--pseudo-cdr3=1:3', datapath('ungrouped.fasta')]
    run(args, resultpath('grouped2.fasta'))


def test_clusterplot(tmpdir):
    main(['clusterplot', '-m', '10', datapath('clusterplot.tab.gz'), str(tmpdir)])
    assert tmpdir.join('IGHV1-1801.png').check()


def test_igblast(run):
    args = ['igblast', '--threads=1', datapath('database/'), datapath('igblast.fasta')]
    run(args, resultpath('assigned.tab'))
