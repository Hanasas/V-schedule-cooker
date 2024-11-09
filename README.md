*祝 nijisanji EN 的 Victoria Brightshield 前程似锦，武运昌隆。*  
*我始终相信vtuber与观众的相遇是一种一期一会的奇迹，如果本项目能为不同国家的vtuber与海外粉丝的相遇变得方便一点点，不胜荣幸。*

Wish you all the best in your future, Victoria.  
I always believe that the encounter between a vtuber and her/his fans is a once-in-a-lifetime miracle.  
I would be honored if this project could make it a little easier for vtubers from different countries to meet their overseas fans.

# 介绍 Introduction

这个项目适用于vtuber字幕组日常的日程表翻译工作。它读取一张日程表原图片，并且将翻译者输入的翻译内容结合到图片，输出一张翻译后的日程表图片。项目会自动换算时间。  
如果您想使用可执行程序，而非源代码,敬请跳到**使用手册**部分浏览
  
This project is suitable for the weekly schedule translation work of the vtuber subtitle group. It reads an original image of a schedule, combines the translation input with the image, and outputs a translated schedule image.The project will automatically convert the time.  
If you prefer to use the executable program instead of the source code, please refer to the **User Manual** section.


# 需求表 requirements  

python = 3.9.0  
easyocr = 1.7.2  
numpy = 2.0.2  
opencv-python = 4.10.0.84  
Pillow = 11.0.0  


# 使用手册 User Manual
首次打开程序时，请在下拉选框选择您的字体和时区  

![font time zone selector](readme_images/image.png)

如果您的时区不在列表中，您可以先随意选择，稍后在程序生成的config.txt中手动修改。注意，您修改的时区可能仍不在程序能换算的列表内，这种情况请联系我
![config.txt](readme_images/image-1.png)

点击确认，字体和时区选择框自动消失，您的信息已经记录到config.txt中了，此后这个窗口不会再出现，如果您需要修改信息，请在文件资源管理器中删除config.txt，重启本程序即可。

在select image窗口，先点击选择图片，在出现的窗口中选择您要翻译的日程表原图片，点击打开，select image窗口会出现图片的预览，确认无误后点击确定
![select image](readme_images/image-2.png)
稍等片刻，此时程序正在运行基于AI的文字识别功能，本程序不使用GPU，因此加载较慢，并非卡死，请耐心等待  
加载完成，窗口标题改为V schedule cooker，可以开始编辑。此时您表中的时间内容应该已经被替换为您选择的时区，如果没有成功替换，或者时差有误（部分时区缩写存在歧义），请联系我修改程序
![cooker](readme_images/image-3.png)
**上一个**、**下一个**按钮会改变当前编辑的文字块，在文本框内输入翻译内容，点击**确定**，当前编辑的文字块会被修改成文本框内的内容  
如果您的窗口中没有出现文本框，按钮或者出现不全，这是由于您选择的图片长宽比不是我预设的16：9，别担心，这不影响使用，请下拉窗口的下边缘找到全部组件，笔者会尽快修改显示问题
![alt text](readme_images/image-5.png)
您可以多次修改同一条文字，但是不推荐这样做，这样可能导致字号异常，不同字块重叠和旧内容覆盖错误等问题  
某些不需要修改的内容也会被识别选中，跳过即可  
在编辑的任何时刻，都可以点击保存并关闭，保存编辑后的图片并关闭本程序


# 特别鸣谢 Special Thanks

Victoria Brightshield  
Victoria的神圣圆桌（在bilibili活动的Victoria Brightshield非官方字幕组）

Special thanks:   
Victoria Brightshield  
Victoria的神圣圆桌(Victoria Brightshield's unofficial subtitle group on bilibili)

# 联系我 Contact Me

如果您在使用本项目时遇到任何问题，或有任何意见和建议，请随时通过gouchengouceq@163.com联系我，或许您也可以在某些vtuber字幕组找到我或者我的联系方式。  
If you encounter any problems when using this project, or have any comments or suggestions, please feel free to contact me at gouchengouceq@163.com. Maybe you can also find me or my contact information in some vtuber subtitle groups.
