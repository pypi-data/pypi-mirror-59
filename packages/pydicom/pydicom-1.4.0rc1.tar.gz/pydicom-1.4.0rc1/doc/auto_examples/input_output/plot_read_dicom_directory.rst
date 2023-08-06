.. note::
    :class: sphx-glr-download-link-note

    Click :ref:`here <sphx_glr_download_auto_examples_input_output_plot_read_dicom_directory.py>` to download the full example code
.. rst-class:: sphx-glr-example-title

.. _sphx_glr_auto_examples_input_output_plot_read_dicom_directory.py:


====================
Read DICOM directory
====================

This example shows how to read DICOM directory.




.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Path to the DICOM directory: c:\git\pydicom\pydicom\data\test_files\dicomdirtests\DICOMDIR
    Patient: 77654033: Doe^Archibald
        Study 2: 20010101: XR C Spine Comp Min 4 Views
            Series 1: CR: N/A (1 image)
                Reading images...

                Image filenames:
                 [           'c:\\git\\pydicom\\pydicom\\data\\test_files\\dicomdirtests\\77654033\\CR1\\6154']
                Patient Names in images..: {'Doe^Archibald'}
                Patient IDs in images..: {'77654033'}
            Series 2: CR: N/A (1 image)
                Reading images...

                Image filenames:
                 [           'c:\\git\\pydicom\\pydicom\\data\\test_files\\dicomdirtests\\77654033\\CR2\\6247']
                Patient Names in images..: {'Doe^Archibald'}
                Patient IDs in images..: {'77654033'}
            Series 3: CR: N/A (1 image)
                Reading images...

                Image filenames:
                 [           'c:\\git\\pydicom\\pydicom\\data\\test_files\\dicomdirtests\\77654033\\CR3\\6278']
                Patient Names in images..: {'Doe^Archibald'}
                Patient IDs in images..: {'77654033'}
        Study 2: 19950903: CT, HEAD/BRAIN WO CONTRAST
            Series 2: CT: N/A (4 images)
                Reading images...

                Image filenames:
                 [           'c:\\git\\pydicom\\pydicom\\data\\test_files\\dicomdirtests\\77654033\\CT2\\17106',
                'c:\\git\\pydicom\\pydicom\\data\\test_files\\dicomdirtests\\77654033\\CT2\\17136',
                'c:\\git\\pydicom\\pydicom\\data\\test_files\\dicomdirtests\\77654033\\CT2\\17166',
                'c:\\git\\pydicom\\pydicom\\data\\test_files\\dicomdirtests\\77654033\\CT2\\17196']
                Patient Names in images..: {'Doe^Archibald'}
                Patient IDs in images..: {'77654033'}
    Patient: 98890234: Doe^Peter
        Study 2: 20010101: 
            Series 4: CT: N/A (2 images)
                Reading images...

                Image filenames:
                 [           'c:\\git\\pydicom\\pydicom\\data\\test_files\\dicomdirtests\\98892001\\CT2N\\6293',
                'c:\\git\\pydicom\\pydicom\\data\\test_files\\dicomdirtests\\98892001\\CT2N\\6924']
                Patient Names in images..: {'Doe^Peter'}
                Patient IDs in images..: {'98890234'}
            Series 5: CT: N/A (5 images)
                Reading images...

                Image filenames:
                 [           'c:\\git\\pydicom\\pydicom\\data\\test_files\\dicomdirtests\\98892001\\CT5N\\2062',
                'c:\\git\\pydicom\\pydicom\\data\\test_files\\dicomdirtests\\98892001\\CT5N\\2392',
                'c:\\git\\pydicom\\pydicom\\data\\test_files\\dicomdirtests\\98892001\\CT5N\\2693',
                'c:\\git\\pydicom\\pydicom\\data\\test_files\\dicomdirtests\\98892001\\CT5N\\3023',
                'c:\\git\\pydicom\\pydicom\\data\\test_files\\dicomdirtests\\98892001\\CT5N\\3353']
                Patient Names in images..: {'Doe^Peter'}
                Patient IDs in images..: {'98890234'}
        Study 428: 20030505: Carotids
            Series 1: MR: N/A (1 image)
                Reading images...

                Image filenames:
                 [           'c:\\git\\pydicom\\pydicom\\data\\test_files\\dicomdirtests\\98892003\\MR1\\15820']
                Patient Names in images..: {'Doe^Peter'}
                Patient IDs in images..: {'98890234'}
            Series 2: MR: N/A (1 image)
                Reading images...

                Image filenames:
                 [           'c:\\git\\pydicom\\pydicom\\data\\test_files\\dicomdirtests\\98892003\\MR2\\15970']
                Patient Names in images..: {'Doe^Peter'}
                Patient IDs in images..: {'98890234'}
        Study 134: 20030505: Brain
            Series 1: MR: N/A (1 image)
                Reading images...

                Image filenames:
                 [           'c:\\git\\pydicom\\pydicom\\data\\test_files\\dicomdirtests\\98892003\\MR1\\4919']
                Patient Names in images..: {'Doe^Peter'}
                Patient IDs in images..: {'98890234'}
            Series 2: MR: N/A (3 images)
                Reading images...

                Image filenames:
                 [           'c:\\git\\pydicom\\pydicom\\data\\test_files\\dicomdirtests\\98892003\\MR2\\4950',
                'c:\\git\\pydicom\\pydicom\\data\\test_files\\dicomdirtests\\98892003\\MR2\\5011',
                'c:\\git\\pydicom\\pydicom\\data\\test_files\\dicomdirtests\\98892003\\MR2\\4981']
                Patient Names in images..: {'Doe^Peter'}
                Patient IDs in images..: {'98890234'}
        Study 2: 20030505: Brain-MRA
            Series 1: MR: N/A (1 image)
                Reading images...

                Image filenames:
                 [           'c:\\git\\pydicom\\pydicom\\data\\test_files\\dicomdirtests\\98892003\\MR1\\5641']
                Patient Names in images..: {'Doe^Peter'}
                Patient IDs in images..: {'98890234'}
            Series 2: MR: N/A (3 images)
                Reading images...

                Image filenames:
                 [           'c:\\git\\pydicom\\pydicom\\data\\test_files\\dicomdirtests\\98892003\\MR2\\6935',
                'c:\\git\\pydicom\\pydicom\\data\\test_files\\dicomdirtests\\98892003\\MR2\\6605',
                'c:\\git\\pydicom\\pydicom\\data\\test_files\\dicomdirtests\\98892003\\MR2\\6273']
                Patient Names in images..: {'Doe^Peter'}
                Patient IDs in images..: {'98890234'}
            Series 700: MR: N/A (7 images)
                Reading images...

                Image filenames:
                 [           'c:\\git\\pydicom\\pydicom\\data\\test_files\\dicomdirtests\\98892003\\MR700\\4558',
                'c:\\git\\pydicom\\pydicom\\data\\test_files\\dicomdirtests\\98892003\\MR700\\4528',
                'c:\\git\\pydicom\\pydicom\\data\\test_files\\dicomdirtests\\98892003\\MR700\\4588',
                'c:\\git\\pydicom\\pydicom\\data\\test_files\\dicomdirtests\\98892003\\MR700\\4467',
                'c:\\git\\pydicom\\pydicom\\data\\test_files\\dicomdirtests\\98892003\\MR700\\4618',
                'c:\\git\\pydicom\\pydicom\\data\\test_files\\dicomdirtests\\98892003\\MR700\\4678',
                'c:\\git\\pydicom\\pydicom\\data\\test_files\\dicomdirtests\\98892003\\MR700\\4648']
                Patient Names in images..: {'Doe^Peter'}
                Patient IDs in images..: {'98890234'}






|


.. code-block:: default


    # authors : Guillaume Lemaitre <g.lemaitre58@gmail.com>
    # license : MIT

    from os.path import dirname, join
    from pprint import pprint

    import pydicom
    from pydicom.data import get_testdata_file
    from pydicom.filereader import read_dicomdir

    # fetch the path to the test data
    filepath = get_testdata_file('DICOMDIR')
    print('Path to the DICOM directory: {}'.format(filepath))
    # load the data
    dicom_dir = read_dicomdir(filepath)
    base_dir = dirname(filepath)

    # go through the patient record and print information
    for patient_record in dicom_dir.patient_records:
        if (hasattr(patient_record, 'PatientID') and
                hasattr(patient_record, 'PatientName')):
            print("Patient: {}: {}".format(patient_record.PatientID,
                                           patient_record.PatientName))
        studies = patient_record.children
        # got through each serie
        for study in studies:
            print(" " * 4 + "Study {}: {}: {}".format(study.StudyID,
                                                      study.StudyDate,
                                                      study.StudyDescription))
            all_series = study.children
            # go through each serie
            for series in all_series:
                image_count = len(series.children)
                plural = ('', 's')[image_count > 1]

                # Write basic series info and image count

                # Put N/A in if no Series Description
                if 'SeriesDescription' not in series:
                    series.SeriesDescription = "N/A"
                print(" " * 8 + "Series {}: {}: {} ({} image{})".format(
                    series.SeriesNumber, series.Modality, series.SeriesDescription,
                    image_count, plural))

                # Open and read something from each image, for demonstration
                # purposes. For simple quick overview of DICOMDIR, leave the
                # following out
                print(" " * 12 + "Reading images...")
                image_records = series.children
                image_filenames = [join(base_dir, *image_rec.ReferencedFileID)
                                   for image_rec in image_records]

                datasets = [pydicom.dcmread(image_filename)
                            for image_filename in image_filenames]

                patient_names = set(ds.PatientName for ds in datasets)
                patient_IDs = set(ds.PatientID for ds in datasets)

                # List the image filenames
                print("\n" + " " * 12 + "Image filenames:")
                print(" " * 12, end=' ')
                pprint(image_filenames, indent=12)

                # Expect all images to have same patient name, id
                # Show the set of all names, IDs found (should each have one)
                print(" " * 12 + "Patient Names in images..: {}".format(
                    patient_names))
                print(" " * 12 + "Patient IDs in images..: {}".format(
                    patient_IDs))


.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  0.340 seconds)


.. _sphx_glr_download_auto_examples_input_output_plot_read_dicom_directory.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download

     :download:`Download Python source code: plot_read_dicom_directory.py <plot_read_dicom_directory.py>`



  .. container:: sphx-glr-download

     :download:`Download Jupyter notebook: plot_read_dicom_directory.ipynb <plot_read_dicom_directory.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
