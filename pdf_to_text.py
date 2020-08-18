from xpdf_python import wrapper

# To be replaced with a universal pdf-text converter
file = '发现报告/1419820.pdf'
text = wrapper.to_text(file)[0]
print(text)

print(text.count('中芯国际'))
