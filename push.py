from tkinter import *
import tkinter.ttk


def switch_to_new_code():
    # 현재 노트북 위젯의 모든 탭 제거
    for tab in notebook.tabs():
        notebook.forget(tab)

    # 새 프레임과 탭 추가
    frame1_new = Frame(window)
    notebook.add(frame1_new, text='페이지1')
    Label(frame1_new, text='페이지1의 내용', fg='red', font='helvetica 48').pack()

    frame2_new = Frame(window)
    notebook.add(frame2_new, text='페이지2')
    Label(frame2_new, text='페이지2의 내용', fg='blue', font='helvetica 48').pack()

    frame3_new = Frame(window)
    notebook.add(frame3_new, text='페이지3')
    Label(frame3_new, text='페이지3의 내용', fg='green', font='helvetica 48').pack()

    frame4_new = Frame(window)
    notebook.add(frame4_new, text='페이지4')
    Label(frame4_new, text='페이지4의 내용', fg='yellow', font='helvetica 48').pack()


# 메인 윈도우 생성
window = Tk()
window.title('노트북')

# Notebook 위젯 생성
notebook = tkinter.ttk.Notebook(window, width=800, height=600)
notebook.pack()

# 초기 프레임 및 탭 추가
frame_initial1 = Frame(window)
notebook.add(frame_initial1, text='초기 페이지1')
Label(frame_initial1, text='초기 페이지1의 내용', fg='red', font='helvetica 48').pack()

# 5초 후에 새로운 코드로 전환
window.after(5000, switch_to_new_code)

# 메인 루프 실행
window.mainloop()