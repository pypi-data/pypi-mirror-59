# TESSERACT2DICT
This class contains two main funtions:

1. **tess2dict**: Input an image and get the extracted text as a dataframe which gives the content, coordinates (x,y,w,h) and confidence of each word. Essentially, it is a wrapper on pytesseract to output a dataframe.
2. **word2text**: Once you obtain the dataframe, you can pass it through this function along with a bounding box to get the text inside the given box with proper formatting.
### Prerequisites

- beautifulsoup4
- [MakeTreeDir](https://github.com/Sreekiranar/MakeTreeDir.git)
- numpy
- opencv-python
- pandas
- pytesseract

### Tesseract Installation
(currently solution works on Tesseract 5.0.0 only)

[What is Tesseract?](https://github.com/tesseract-ocr/tesseract)
#### For Windows
- [installation link](https://github.com/UB-Mannheim/tesseract/wiki)
##### adding path to path variable (for Tesseract)
- [windows 10](https://helpdeskgeek.com/windows-10/add-windows-path-environment-variable/)
- [windows 7](https://docs.alfresco.com/4.2/tasks/fot-addpath.html)

#### For Linux
- `sudo apt install tesseract-ocr`
- `sudo apt install libtesseract-dev`


### Installation

`pip install tesseract2dict`


### Usage
A sample usage of our solution is shown below. Input an image as numpy.ndarray and the extracted
dataframe at word level is returned.
You can also get the text as plain of a given bounding box with proper formatting using the second function
eg:
```python
import cv2
from tesseract2dict import TessToDict
td=TessToDict()
inputImage=cv2.imread('path/to/image.jpg')
### function 1
word_dict=td.tess2dict(inputImage,'out','outfolder')

### function 2
text_plain=td.word2text(word_dict,(0,0,inputImage.shape[1],inputImage.shape[0]))

```

## Authors

* **Sreekiran A R** - *Analytics Consultant, AI Labs, Bridgei2i Analytics Solutions* -
 [Github](https://github.com/Sreekiranar) ,
[Stackoverflow](https://stackoverflow.com/users/9605907/sreekiran)

* **Anil Prasad M N** - *Project Manager, AI Labs, Bridgei2i Analytics Solutions* -
 [Github](https://github.com/anilprasadmn)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

NOTE: This software depends on other packages that may be licensed under different open source licenses.

### Useful links
1. http://gwang-cv.github.io/2017/08/25/ubuntu16.04+Tesseract4.0/
