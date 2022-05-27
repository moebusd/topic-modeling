from setuptools import setup
import urllib


setup(
        name='topic_modeling',
        version=urllib.request.urlopen("https://github.com/moebusd/topic-modeling/blob/main/version.txt"),
        author="Dennis Möbus",
        author_email="dennis.moebus@fernuni-hagen.de",
        url="https://github.com/moebusd/topic-modeling",
        description="modules of topic modeling pipeline as developed by the research group digital humanities at FernUniversität in Hagen",
        long_description=readme,
        python_requires=">=3.6",
        cmdclass={
          'upload': UploadCommand,
        },
    )
