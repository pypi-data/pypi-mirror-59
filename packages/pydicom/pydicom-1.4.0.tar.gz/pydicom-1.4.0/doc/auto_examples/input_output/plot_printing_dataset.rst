.. note::
    :class: sphx-glr-download-link-note

    Click :ref:`here <sphx_glr_download_auto_examples_input_output_plot_printing_dataset.py>` to download the full example code
.. rst-class:: sphx-glr-example-title

.. _sphx_glr_auto_examples_input_output_plot_printing_dataset.py:


==========================================
Format the output of the data set printing
==========================================

This example illustrates how to print the data set in your own format.




.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


     Image Type = ['DERIVED', 'SECONDARY', 'OTHER']
     Instance Creation Date = '20040826'
     Instance Creation Time = '185434'
     Instance Creator UID = '1.3.6.1.4.1.5962.3'
     SOP Class UID = '1.2.840.10008.5.1.4.1.1.4'
     SOP Instance UID = '1.3.6.1.4.1.5962.1.1.4.1.1.20040826185059.5457'
     Study Date = '20040826'
     Series Date = ''
     Acquisition Date = ''
     Study Time = '185059'
     Series Time = ''
     Acquisition Time = ''
     Accession Number = ''
     Modality = 'MR'
     Manufacturer = 'TOSHIBA_MEC'
     Institution Name = 'TOSHIBA'
     Referring Physician's Name = ''
     Timezone Offset From UTC = '-0400'
     Station Name = '000000000'
     Name of Physician(s) Reading Study = '----'
     Operators' Name = '----'
     Manufacturer's Model Name = 'MRT50H1'
     Patient's Name = 'CompressedSamples^MR1'
     Patient ID = '4MR1'
     Patient's Birth Date = ''
     Patient's Sex = 'F'
     Patient's Size = None
     Patient's Weight = "80.0"
     Contrast/Bolus Agent = ''
     Scanning Sequence = 'SE'
     Sequence Variant = 'NONE'
     Scan Options = ''
     MR Acquisition Type = '3D'
     Slice Thickness = "0.8"
     Repetition Time = "4000.0"
     Echo Time = "240.0"
     Number of Averages = "1.0"
     Imaging Frequency = "63.924339"
     Imaged Nucleus = 'H'
     Echo Number(s) = "1"
     Echo Train Length = None
     Device Serial Number = '-0000200'
     Software Versions = 'V3.51*P25'
     Flip Angle = "90.0"
     Patient Position = 'HFS'
     Study Instance UID = '1.3.6.1.4.1.5962.1.2.4.20040826185059.5457'
     Series Instance UID = '1.3.6.1.4.1.5962.1.3.4.1.20040826185059.5457'
     Study ID = '4MR1'
     Series Number = "1"
     Acquisition Number = "0"
     Instance Number = "1"
     Image Position (Patient) = [-83.9063, -91.2000, 6.6406]
     Image Orientation (Patient) = [1.0000, 0.0000, 0.0000, 0.0000, 1.0000, 0.0000]
     Frame of Reference UID = '1.3.6.1.4.1.5962.1.4.4.1.20040826185059.5457'
     Laterality = ''
     Position Reference Indicator = ''
     Slice Location = "0.0"
     Image Comments = 'Uncompressed'
     Samples per Pixel = 1
     Photometric Interpretation = 'MONOCHROME2'
     Rows = 64
     Columns = 64
     Pixel Spacing = [0.3125, 0.3125]
     Bits Allocated = 16
     Bits Stored = 16
     High Bit = 15
     Pixel Representation = 1
     Smallest Image Pixel Value = 0
     Largest Image Pixel Value = 4000
     Window Center = "600.0"
     Window Width = "1600.0"
    <item not printed -- in the "don't print" list>
     Data Set Trailing Padding = b'\n\x00\xfe\x00\x04\x00\x01\x00\x00\x00\x00\x00\x...






|


.. code-block:: default


    # authors : Guillaume Lemaitre <g.lemaitre58@gmail.com>
    # license : MIT

    from __future__ import print_function

    import pydicom
    from pydicom.data import get_testdata_files

    print(__doc__)


    def myprint(dataset, indent=0):
        """Go through all items in the dataset and print them with custom format

        Modelled after Dataset._pretty_str()
        """
        dont_print = ['Pixel Data', 'File Meta Information Version']

        indent_string = "   " * indent
        next_indent_string = "   " * (indent + 1)

        for data_element in dataset:
            if data_element.VR == "SQ":   # a sequence
                print(indent_string, data_element.name)
                for sequence_item in data_element.value:
                    myprint(sequence_item, indent + 1)
                    print(next_indent_string + "---------")
            else:
                if data_element.name in dont_print:
                    print("""<item not printed -- in the "don't print" list>""")
                else:
                    repr_value = repr(data_element.value)
                    if len(repr_value) > 50:
                        repr_value = repr_value[:50] + "..."
                    print("{0:s} {1:s} = {2:s}".format(indent_string,
                                                       data_element.name,
                                                       repr_value))


    filename = get_testdata_files('MR_small.dcm')[0]
    ds = pydicom.dcmread(filename)

    myprint(ds)


.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  0.019 seconds)


.. _sphx_glr_download_auto_examples_input_output_plot_printing_dataset.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download

     :download:`Download Python source code: plot_printing_dataset.py <plot_printing_dataset.py>`



  .. container:: sphx-glr-download

     :download:`Download Jupyter notebook: plot_printing_dataset.ipynb <plot_printing_dataset.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
