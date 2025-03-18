# 先引入要使用的第三方库
import time
import xlrd
import pyautogui
import pyperclip
# 对数据进行验证
def dataCheck(sheetdata):
    # 开始检测
    checked = True
    # 如果我的行小于2就报错
    if sheetdata.nrows < 2:
        print('数据只有标题,没有内容,请重新选择')
        checked = False
    # 开始循环查询,设置一个标识数
    i = 1
    while i < sheetdata.nrows:
        # 开始拿第二行的第一位, 第一行的索引是0
        opacity_item = sheetdata.row(i)[0]
        # 先判断我输入的是不是数字
        opacity_type = opacity_item.ctype
        if opacity_type != 2:
            print('第', i+1, '行有问题,请查看,输入的不是数字')
            checked = False
        # 判断我输入的数字是否合规
        opacity_value = opacity_item.value
        if opacity_value > 9 and opacity_value < 0:
            #证明数字不对
            print('第', i+1, '行有问题,请查看, 输入的数字不合规')
            checked = False
        # 证明没问题了,那么就可以看第二项了,第二项是时间和滚动时长,这个得看是不是长按和滚动
        opacity_second_item = sheetdata.row(i)[1]
        # 拿到它的类型
        opacity_second_type = opacity_second_item.ctype
        if opacity_value != 3 and opacity_value != 4 and opacity_value != 6 and opacity_value != 7 and opacity_value != 9 and opacity_value != 10:
            # 这个地方不应该是数字,应该是空的
            if opacity_second_type == 2:
                print('第', i+1, '行有问题,请查看, 此项不应该有值')
                checked = False
        #到这就是没问题了
        i += 1
    return checked

currentClickIsWarehouse = True

# 鼠标操作
def mouseClick(clickTime, clickEvent, img, reTry, scrollWidth):
    print('点击的次数,还有这这那那的,先不管,先写下面')
    global currentX, currentY, currentClickIsWarehouse
    # 等于1就是点击类的
    if reTry == 1:
        while True:
            if clickEvent == 'one_left':
                # 这个地方判断下我鼠标的复制内容是什么
                copy_value = pyperclip.paste()
                # 判断如果复制的值是CA FL NY TX时 不走下面的,走我另一个
                if copy_value in ['CA','FL','NY','TX']:
                    if currentClickIsWarehouse and img != './operation_pic/edge.jpg':
                        #  证明是复制了仓库的数据的，要把那个状态更新
                        currentClickIsWarehouse = False
                    elif currentClickIsWarehouse == False and img != './operation_pic/edge.jpg':
                        #  第二次进来的时候 因为状态已经更新了,所以我要把状态更新回去,并且开始找图片
                        currentClickIsWarehouse = True
                        try:
                            print(copy_value, './operation_pic/' + copy_value + '.jpg')
                            location = pyautogui.locateCenterOnScreen('./operation_pic/' + copy_value + '.jpg', confidence=0.8)
                            if location is not None:
                                # 证明我找到了,那么就可以操作
                                pyautogui.click(location.x, location.y, clicks=clickTime,interval=0.2,duration=0.2,button="left")
                                break
                        except pyautogui.ImageNotFoundException:
                            time.sleep(2)
                            print('暂时找不到图片,找不到就退出去了,有问题')
                            pyperclip.copy('123')
                            break
                try:
                    location = pyautogui.locateCenterOnScreen(img, confidence=0.9)
                    if location is not None:
                        # 证明我找到了,那么就可以操作
                        pyautogui.click(location.x, location.y, clicks=clickTime,interval=0.2,duration=0.2,button="left")
                        currentX = location.x
                        currentY = location.y
                        break
                except pyautogui.ImageNotFoundException:
                    # 找不到图片,那么就等待
                    time.sleep(2)
                    print('暂未找到匹配的图片,请稍后再试')
            elif clickEvent == 'double_left':
                try:
                    location = pyautogui.locateCenterOnScreen(img, confidence=0.9)
                    if location is not None:
                        # 证明我找到了,那么就可以操作 双击操作不要添加interval 不然会无效
                        pyautogui.doubleClick(location.x, location.y)
                        currentX = location.x
                        currentY = location.y
                        break
                except pyautogui.ImageNotFoundException:
                    # 找不到图片,那么就等待
                    time.sleep(2)
                    print('暂未找到匹配的图片,请稍后再试')
            elif clickEvent == 'mouse_scroll':
                # 这个地方直接滚动就行,都不用识别的
                pyautogui.scroll(scrollWidth)
                break
            elif clickEvent == 'mouse_copy':
                pyautogui.hotkey('ctrl', 'c')
                break
            elif clickEvent == 'mouse_pause':
                pyautogui.hotkey('ctrl', 'v')
                break

#弄个全局的xy, 就是可以看到我当前的图片位置
currentX = 0
currentY = 0
# 进行操作
def mainWork(sheetdata):
    i = 1
    while i < sheetdata.nrows:
        global currentX, currentY
        # 执行第一行的指令
        print('我现在正在执行', i + 1, '行指令')
        # 判断不同的数字,有不同的操作
        # 先拿到第一行第一个单元格
        opacity_item = sheetdata.row(i)[0]
        # 拿到值
        opacity_value = opacity_item.value
        # 判断是什么操作
        if opacity_value == 1:
            # 单击
            # 取图片名称
            imgName = sheetdata.row(i)[2].value
            mouseClick(1, "one_left", imgName, 1, 0)
        elif opacity_value == 2:
            # 双击
            # 取图片名称
            imgName = sheetdata.row(i)[2].value
            mouseClick(1, "double_left", imgName, 1, 0)
        elif opacity_value == 3:
            # 滚动 第五个参数是滚动的格数
            mouseClick(1, "mouse_scroll", '', 1, -5)
        elif opacity_value == 4:
            # 如果有值,直接在这里copy就行
            copy_value = sheetdata.row(i)[1]
            print(copy_value)
            if copy_value.ctype == 2:
                pyperclip.copy(copy_value)
                i += 1
                continue
            mouseClick(1, "mouse_copy", '', 1, 0)
        elif opacity_value == 5:
            mouseClick(1, "mouse_pause", '', 1, 0)
        elif opacity_value == 7:
            # 等待
            time.sleep(sheetdata.row(i)[1].value)
        elif opacity_value == 8:
            operator_List = sheetdata.row(i)[2].value
            operator_item = operator_List.split(',')
            operator_index = 0
            isGoing = True
            NoScroll = True
            # 这个地方要去循环,直到拿不到东西为止
            while isGoing:
                operator_index = 0
                while operator_index < len(operator_item):
                    # 证明要循环了 这个地方要先判断是字符串还是数字
                    if len(operator_item[operator_index].split(' ')) >= 2:
                        print('这个地方要移动')
                        # 证明要移动, 拿值
                        move_value = operator_item[operator_index].split(' ')
                        # 第一个值是x, 第二个值是y
                        # 证明我找到了,那么就可以操作
                        if len(move_value) >= 3:
                            if move_value[2] == 'cv':
                                # 斜向下移动鼠标
                                pyautogui.moveRel(-20, 15, duration=1)
                            if move_value[2] == 'own':
                                # 拿到第三个位置的值
                                m_v = sheetdata.row(i)[2].value
                                # 拿到x和y
                                x_y_value = m_v.split(' ')
                                pyautogui.moveRel(int(x_y_value[0]), int(x_y_value[1]), duration=1)
                            # 证明是要复制东西 这个是按下鼠标左键
                            pyautogui.mouseDown(button='left')
                            pyautogui.moveRel(int(move_value[0]), int(move_value[1]), duration=1)
                            # 释放鼠标左键
                            pyautogui.mouseUp(button='left')
                        else:
                            print(move_value[0], currentX)
                            pyautogui.click(currentX - int(move_value[0]), currentY - int(move_value[1]), clicks=1,interval=0.2,duration=0.2,button="left")
                    elif len(operator_item[operator_index]) == 1:
                        print('要等待')
                        time.sleep(int(operator_item[operator_index]))
                    else:
                        try:
                            location = pyautogui.locateCenterOnScreen(operator_item[operator_index], confidence=0.8)
                            if location is not None:
                                # 证明我找到了,那么就可以操作
                                pyautogui.click(location.x, location.y, clicks=1,interval=0.2,duration=0.2,button="left")
                                currentX = location.x
                                currentY = location.y
                                time.sleep(1)
                                # 这个地方重置下我的滚动
                                NoScroll = True
                        except pyautogui.ImageNotFoundException:
                            # 找不到图片,那么就等待
                            time.sleep(2)
                            print(operator_item[operator_index])
                            print('暂未找到匹配的图片,请稍后再试')
                            # 这个地方可能是找不到了,所以会再操作一下,滚动下,如果还没有就是结束了
                            if NoScroll:
                                mouseClick(1, "mouse_scroll", '', 1, -100)
                                NoScroll = False
                                print("重新开始了嗷")
                                operator_index = 0
                                continue
                            isGoing = False
                    operator_index += 1    
        elif opacity_value == 9:
            # 证明要移动, 拿值
            move_value = sheetdata.row(i)[1].value.split(' ')
            # 第一个值是x, 第二个值是y
            # 证明我找到了,那么就可以操作
            if len(move_value) >= 3:
                if move_value[2] == 'cv':
                    # 斜向下移动鼠标
                    pyautogui.moveRel(-20, 15, duration=1)
                if move_value[2] == 'own':
                    # 拿到第三个位置的值
                    m_v = sheetdata.row(i)[2].value
                    # 拿到x和y
                    x_y_value = m_v.split(' ')
                    pyautogui.moveRel(int(x_y_value[0]), int(x_y_value[1]), duration=1)
                # 证明是要复制东西 这个是按下鼠标左键
                pyautogui.mouseDown(button='left')
                pyautogui.moveRel(int(move_value[0]), int(move_value[1]), duration=1)
                # 释放鼠标左键
                pyautogui.mouseUp(button='left')
            else:
                pyautogui.click(currentX - int(move_value[0]), currentY - int(move_value[1]), clicks=1,interval=0.2,duration=0.2,button="left")
        elif opacity_value == 10:
            for_num = sheetdata.row(i)[1]
            if for_num.ctype == 2:
                # 证明要循环
                j = 1
                while j <= int(for_num.value):
                    pyautogui.hotkey(sheetdata.row(i)[2].value)
                    j += 1
            else:
                # 拿第三个值
                opacity_item = sheetdata.row(i)[2].value
                opacity_list = opacity_item.split(' ')
                for key in opacity_list:
                    compare_item = key.split('+')
                    if len(compare_item) > 1:
                        pyautogui.hotkey(compare_item[0], compare_item[1])
                    else:
                        pyautogui.hotkey(compare_item[0])

        i += 1
# 初始化
if __name__ == '__main__':
    # 这个是错误件操作的
    # file = 'shipout_fail.xls'
    # 这个是正常流程操作的
    file = 'tiktok.xls' 
    # 这次多次操作的第二次开始操作的
    # file = 'ticket.xls'
    # 测试代码
    # file = 'demo.xls'
    #打开文件
    wb = xlrd.open_workbook(filename=file)
    #通过索引获取表格sheet页
    sheet1 = wb.sheet_by_index(0)
    # 看一眼数据
    print("这是数据", sheet1)
    print('欢迎使用呆呆的自动化程序,正在进行数据检测')
    #数据检查
    checkCmd = dataCheck(sheet1)
    print('检查结果为', checkCmd)
    if checkCmd:
        # 证明数据是对的, 看看用户要进行什么操作
        key = input("请选择你要操作的业务\n1.自动化发货\n2.自动化摸鱼\n")
        if key == '1':
            # 证明要搞自动化,那么就调用我的函数来操作
            print('自动化发货流程正在初始化,请稍后')
            mainWork(sheet1)
        elif key == '2':
            print('正要发单ing~')
            k = 1
            while k <= 16:
                # 读取第二个文件
                if k >= 2:
                    file = 'ticket.xls'
                    wb = xlrd.open_workbook(filename=file)
                    sheet1 = wb.sheet_by_index(0)
                k += 1
                mainWork(sheet1) 