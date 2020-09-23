from xpdf_python import wrapper


if __name__ == '__main__':
    # To be replaced with a universal pdf-text converter
    file = 'cache/中芯国际/report/萝卜投研/4175690.pdf'
    text = wrapper.to_text(file)[0]
    print(text)

# print(text.count('中芯国际'))
