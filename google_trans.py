# from googletrans import Translator

# def gg_trans(raw, en2cn=True):
#     """使用googletrans将英文翻译成中文或者将中文翻译成英文(en2cn=False)."""
#     translator = Translator(service_urls=["translate.google.cn"])
#     if en2cn:
#         text = translator.translate(raw, src="en", dest="zh-cn").text
#     else:
#         text = translator.translate(raw, src="zh-cn", dest="en").text
#     return common.punctuator(text)
