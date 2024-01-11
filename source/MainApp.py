import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import base64
import subprocess
import os
import sqlite3
import Client
import initDatabase

class mailApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mail Client")
        self.frames = {}
        self.mailBoxWindow = None
        self.mailContent = None
        self.senderMailVar = tk.StringVar()
        self.recipientMailVar = tk.StringVar()
        self.ccMailVar = tk.StringVar()
        self.bccMailVar = tk.StringVar()
        self.subjectVar = tk.StringVar()
        self.filePathsVar = tk.StringVar()
        self.messageBodyVar = None
        self.autoDownloadId = None
        self.autoLoadTime = Client.config["autoLoadTime"]
        self.createMailApp()

    def createMailApp(self):
        labelFrom = ttk.Label(self.root, text="From:", foreground="red")
        labelFrom.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        entryFrom = ttk.Entry(self.root, width=30, textvariable=self.senderMailVar)
        entryFrom.grid(row=0, column=1, padx=10, pady=5)

        labelTo = ttk.Label(self.root, text="To:", foreground="red")
        labelTo.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

        entryTo = ttk.Entry(self.root, width=30, textvariable=self.recipientMailVar)
        entryTo.grid(row=1, column=1, padx=10, pady=5)

        labelCc = ttk.Label(self.root, text="Cc:")
        labelCc.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

        entryCc = ttk.Entry(self.root, width=30, textvariable=self.ccMailVar)
        entryCc.grid(row=2, column=1, padx=10, pady=5)

        labelBcc = ttk.Label(self.root, text="Bcc:")
        labelBcc.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

        entryBcc = ttk.Entry(self.root, width=30, textvariable=self.bccMailVar)
        entryBcc.grid(row=3, column=1, padx=10, pady=5)

        labelSubject = ttk.Label(self.root, text="Subject:", foreground="red")
        labelSubject.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)

        entrySubject = ttk.Entry(self.root, width=30, textvariable=self.subjectVar)
        entrySubject.grid(row=4, column=1, padx=10, pady=5)

        labelMessage = ttk.Label(self.root, text="Message:", foreground="red")
        labelMessage.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)

        textMessage = tk.Text(self.root, width=30, height=10)
        textMessage.grid(row=5, column=1, padx=10, pady=5)
        self.messageBodyVar = textMessage

        labelAttachment = ttk.Label(self.root, text="Attachment:")
        labelAttachment.grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)

        entryAttachment = ttk.Entry(self.root, width=45, textvariable=self.filePathsVar)
        entryAttachment.grid(row=6, column=1, padx=10, pady=5)

        buttonAttach = ttk.Button(self.root, text="Attach File", command=self.attachFile)
        buttonAttach.grid(row=6, column=2, padx=10, pady=5)

        buttonSendMail = ttk.Button(self.root, text="Send Mail", command=self.handleSendMail)
        buttonSendMail.grid(row=7, column=0, columnspan=2, pady=10)

        buttonShowMailBox = ttk.Button(self.root, text="Mail Box", command=self.showMailBox)
        buttonShowMailBox.grid(row=7, column=2, padx=10, pady=5)

        self.root.mainloop()
        
    def autoDownloadMail(self):
        try:
            hadNewMail = Client.receiveMail()
            if hadNewMail:
                newData = self.getData()
                self.showMailList(newData)
        except Exception as e:
            pass
        self.autoDownloadId = self.root.after(self.autoLoadTime, self.autoDownloadMail)
        
        
    def stopAutoDownloadMail(self):
        if self.autoDownloadId:
            self.root.after_cancel(self.autoDownloadId)
        if self.mailBoxWindow:
            self.mailBoxWindow.destroy()
            
    def attachFile(self):
        newFilePaths = filedialog.askopenfilenames(title="Select Files")
        currentFilePaths = self.filePathsVar.get().split(";") if self.filePathsVar.get() else []

        for filePath in newFilePaths:
            size = os.path.getsize(filePath) / (1024 * 1024)
            if size <= Client.config["maxSize"]:
                currentFilePaths.append(filePath)
            else:
                messagebox.showerror("Error", f"Unable to send files larger than {Client.config['maxSize']} MB")

        self.filePathsVar.set(";".join(currentFilePaths))

    def handleSendMail(self):
        senderMail = self.senderMailVar.get()
        recipientMail = self.recipientMailVar.get().split(' ')
        ccMail = self.ccMailVar.get().split(' ')
        bccMail = self.bccMailVar.get().split(' ')
        subject = self.subjectVar.get()
        messageBody = self.messageBodyVar.get("1.0", "end-1c")
        filePaths = self.filePathsVar.get()
        
        if not senderMail or not recipientMail or not subject or not messageBody:
            messagebox.showerror("Error", "Please fill in all required fields.")
            return
        
        if len(filePaths) != 0:
            filePaths = filePaths.split(';')
        
        try:
            Client.sendMail(senderMail, recipientMail, ccMail,
                            bccMail, subject, messageBody, filePaths)
            messagebox.showinfo("Success", "Email sent successfully!")
        except Exception as e:
            pass
        
    def onFileSelected(self, event, filePath, fileContent):
        try:
            folderPath = "./file"
            if not os.path.exists(folderPath):
                os.makedirs(folderPath)
            savePath = os.path.join(folderPath, filePath)
            content = base64.b64decode(fileContent)
            with open(savePath, 'wb') as file:
                file.write(content)
            subprocess.Popen(['start', savePath], shell=True)
        except Exception as e:
            pass
    def onMailSelected(self, event, folder):
        selectedItem = event.widget.selection()[0]
        values = list((event.widget.item(selectedItem, 'values')))
        _from = values[1]
        subject = values[2]
        content = values[5]
        to = " ".join(eval(values[3]))
        cc = " ".join(eval(values[4]))
        filePaths = eval(values[-3])
        fileContents = eval(values[-2])
        height = 460 + len(filePaths) * 15
        id = values[-1]
        status = values[0]
        self.mailContent = tk.Toplevel()
        self.mailContent.title("Mail Content")
        self.mailContent.geometry(f"450x{height}")
        senderLabel = tk.Label(self.mailContent, text=f"Sender: {_from}")
        senderLabel.pack(anchor=tk.W, pady=5, padx=20)
        toLabel = tk.Label(self.mailContent, text=f"To: {to}")
        toLabel.pack(anchor=tk.W, pady=5, padx=20)
        ccLabel = tk.Label(self.mailContent, text=f"Cc: {cc}")
        ccLabel.pack(anchor=tk.W, pady=5, padx=20)
        subjectLabel = tk.Label(self.mailContent, text=f"Subject: {subject}")
        subjectLabel.pack(anchor=tk.W, padx=20)
        labelMessage = ttk.Label(self.mailContent, text="Message:")
        labelMessage.pack(anchor=tk.W, padx=20)
        textMessage = tk.Text(self.mailContent, wrap=tk.WORD, width=40, height=15)
        textMessage.insert(tk.END, content)
        textMessage.pack()
        if len(filePaths) != 0:
            number = len(filePaths)
            attachmentLabel = ttk.Label(self.mailContent, text=f"Have {number} attachments:")
            attachmentLabel.pack(anchor=tk.W, padx=20)

            for idx in range(len(filePaths)):
                fileLabel = ttk.Label(self.mailContent, text=filePaths[idx], cursor="hand2", foreground="red")
                fileLabel.pack(anchor=tk.W, padx=20)
                fileLabel.bind("<Button-1>", lambda event, filePath=filePaths[idx], fileContent=fileContents[idx]: self.onFileSelected(event, filePath, fileContent))
        buttonFrame = ttk.Frame(self.mailContent)
        buttonFrame.pack(pady=10)

        if len(filePaths) != 0:
            buttonAttach = ttk.Button(buttonFrame, text="Download file", command=lambda: self.handleDownloadFile(filePaths, fileContents))
            buttonAttach.pack(side=tk.LEFT, padx=10)

        buttonMove = ttk.Button(buttonFrame, text="Move", command=lambda: self.showContextMenu(id, folder))
        buttonMove.pack(side=tk.LEFT, padx=10)

        folders = Client.config["mailFolder"]
        connection = sqlite3.connect(f'./database/{Client.dataBaseFile}')
        cursor = connection.cursor()
        for item in folders:
            cursor.execute(f"UPDATE {item} SET [status] = ? WHERE id = ?", ("Seen", id))
        connection.commit()
        connection.close()
        if status == "Not Seen":
            newData = self.getData()
            self.showMailList(newData)

    def showContextMenu(self, id, folder):
        folders = Client.config["mailFolder"]
        context_menu = tk.Menu(self.mailBoxWindow, tearoff=0)
        for destination_folder in folders:
            if destination_folder != folder:
                context_menu.add_command(label=f'Move to {destination_folder} folder', command=lambda sourceFolder=folder, destFolder=destination_folder, id=id: self.onContextMenuClicked(sourceFolder, destFolder, id))
        context_menu.post(self.mailBoxWindow.winfo_pointerx(), self.mailBoxWindow.winfo_pointery())

    def onContextMenuClicked(self, sourceFolder, destFolder, id):
        connection = sqlite3.connect(f'./database/{Client.dataBaseFile}')
        cursor = connection.cursor()
        cursor.execute(f'select * from {sourceFolder} where id={id}')
        mail = list(cursor.fetchall()[0])
        folders = Client.config["mailFolder"]
        for item in folders:
            cursor.execute(f'DELETE FROM {item} WHERE id = {id}')
        Client.insertToDatabase(connection, "Seen", mail[1], mail[2], mail[3], mail[4], mail[5], mail[6], mail[7], mail[-1], destFolder)
        if self.mailContent:
            self.mailContent.destroy()
        newData = self.getData()
        self.showMailList(newData)
        connection.close()
        
    def handleDownloadFile(self, filePaths, fileContents):
        saveFolder = filedialog.askdirectory()
        for index in range(0, len(filePaths), 1):
            fileName = os.path.basename(filePaths[index])
            savePath = os.path.join(saveFolder, fileName)
            try:
                content = base64.b64decode(fileContents[index])
                with open(savePath, 'wb') as file:
                    file.write(content)
            except Exception as e:
                pass
    
    def showMailBox(self):
        self.mailBoxWindow = tk.Toplevel()
        self.mailBoxWindow.title("Mail Box")
        self.mailBoxWindow.geometry("650x400")
        
        for frame in self.frames.values():
            frame.destroy()
        mailData = self.getData()
        self.showMailList(mailData)
        buttonReceive = ttk.Button(self.mailBoxWindow, text="Download Mail", command=self.updateData)
        buttonReceive.grid(row=1, column=0, pady=5)
        self.autoDownloadMail()
        self.mailBoxWindow.protocol("WM_DELETE_WINDOW", self.stopAutoDownloadMail)
        
    def showMailList(self, mailData):
        notebook = ttk.Notebook(self.mailBoxWindow)
        notebook.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)
        folders = Client.config["mailFolder"]
        self.frames = {folder: ttk.Frame(notebook) for folder in folders}

        for folder in folders:
            notebook.add(self.frames[folder], text=folder)
            tree = ttk.Treeview(self.frames[folder], columns=("Status", "Sender", "Subject"), show="headings")
            tree.heading("Status", text="Status")
            tree.heading("Sender", text="Sender")
            tree.heading("Subject", text="Subject")

            for data in mailData.get(folder, []):
                mail = list(data)
                tree.insert("", tk.END, values=mail)
                tree.bind("<<TreeviewSelect>>", lambda event, folder=folder: self.onMailSelected(event, folder))

            tree.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)
    def getData(self):
        connection = sqlite3.connect(f'./database/{Client.dataBaseFile}')
        cursor = connection.cursor()
        mailData = {}
        folders = Client.config["mailFolder"]
        for folder in folders:
            cursor.execute(f"select * from {folder}")
            dataInFolder = cursor.fetchall()
            mailData.update({folder: dataInFolder})
        cursor.close()
        connection.close()
        return mailData
    def updateData(self):
        try:
            hadNewMail = Client.receiveMail()
            if hadNewMail:
                newData = self.getData()
                self.showMailList(newData)
                messagebox.showinfo("Success", "Mail downloaded successfully!")
        except Exception as e:
            pass
        
if __name__ == "__main__": 
    if os.path.isfile(f'./database/{Client.dataBaseFile}') == False:
        initDatabase.initDataBase()
    app = mailApp()
