from xpdf_python import wrapper

# To be replaced with a universal pdf-text converter
file = 'cache/萝卜投研/3694293.pdf'
text = wrapper.to_text(file)[0]
print(text)

# print(text.count('中芯国际'))
