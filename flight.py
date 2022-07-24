import tkinter as tk
import mysql.connector

db=mysql.connector.connect(host="localhost",user="root",passwd="admin",database="bookingsystem")
cursor=db.cursor()

def sync():
    cursor.execute("select username,password from users where role='admin'")
    result = cursor.fetchone()
    global admin
    admin = {result[0]: result[1]}

    cursor.execute("select username,password from users where role='user'")
    result = cursor.fetchall()
    global standard
    standard={}
    for i in result:
        username = i[0]
        password = i[1]
        standard[username]=password

    cursor.execute("select * from flights where status='scheduled' or status='delayed'")
    result1 = cursor.fetchall()
    global scheduled
    scheduled={}
    for i in result1:
        flightno = i[0]
        departure = i[1]
        destination = i[2]
        status = i[3]
        scheduled[flightno]=[departure,destination,status]

    cursor.execute("select * from flights where status='cancelled'")
    result1 = cursor.fetchall()
    global cancelled
    cancelled={}
    for i in result1:
        flightno = i[0]
        departure = i[1]
        destination = i[2]
        status = i[3]
        cancelled[flightno]=[departure,destination,status]

def display_users():
    display_scheduled = tk.Tk()
    display_scheduled.title("View Users")

    display_scheduled['background']='#1c1c1c'
    tk.Label(master=display_scheduled, bg="#1c1c1c",text="").grid(row=0, column=1)
    e =2
    tk.Label(master=display_scheduled,bg="#1c1c1c", fg= "#fafaff",font="ubuntu", text="Standard Users Are:").grid(row=1, column=0)
    tk.Label(master=display_scheduled, bg="#1c1c1c",text="").grid(row=2, column=1)
    for a in standard:
        e += 1
        tk.Label(master=display_scheduled,bg="#1c1c1c", fg= "#fafaff", text=("-----", a)).grid(row=e, column=0)

def update():
    def update_btn1():
        if number_of_flight.get() in scheduled:
            flightno = number_of_flight.get()
            departure = departure_time.get()
            status = stat.get()
            destination = destination_place.get()
            cursor.execute("update flights set departure_time='%s',destination='%s',status='%s' where flightno='%s';"%(departure,destination,status,flightno))
            db.commit()
            update_root = tk.Tk()
            update_root.title("Successfully Updated!")
            update_root['background']='#1c1c1c'
            tk.Label(master=update_root, bg="#1c1c1c",text="").grid(row=0, column=1)
            tk.Label(master=update_root,bg="#1c1c1c", fg= "#fafaff",font="ubuntu", text="Successfully Updated!!").grid(row=1, column=0)
            tk.Label(master=update_root, bg="#1c1c1c",text="").grid(row=2, column=1)
            sync()
            scheduled_update.destroy()
        else:
            flightno = number_of_flight.get()
            departure = departure_time.get()
            status = stat.get()
            destination = destination_place.get()
            cursor.execute("insert into flights values('%s','%s','%s','%s')"%(flightno,departure,destination,status))
            db.commit()
            update_root = tk.Tk()
            update_root.title("Successfully Added!")
            update_root['background']='#1c1c1c'
            tk.Label(master=update_root, bg="#1c1c1c",text="").grid(row=0, column=1)
            tk.Label(master=update_root,bg="#1c1c1c", fg= "#fafaff",font="ubuntu", text="Successfully Updated!!").grid(row=1, column=0)
            tk.Label(master=update_root, bg="#1c1c1c",text="").grid(row=2, column=1)
            sync()
            scheduled_update.destroy()

    scheduled_update = tk.Tk()
    scheduled_update.title("Update/Add A Flight")
    scheduled_update['background']='#1c1c1c'
    tk.Label(master=scheduled_update, bg="#1c1c1c",text="").grid(row=1, column=1)
    tk.Label(master=scheduled_update,bg="#1c1c1c", fg= "#fafaff",font="ubuntu", text="Enter The Flight Number:").grid(row=2, column=0)
    number_of_flight = tk.Entry(master=scheduled_update)
    number_of_flight.grid(row=2, column=1)
    tk.Label(master=scheduled_update, bg="#1c1c1c",text="").grid(row=3, column=1)
    tk.Label(master=scheduled_update,bg="#1c1c1c", fg= "#fafaff",font="ubuntu", text="Enter Departure Time:").grid(row=4, column=0)
    departure_time = tk.Entry(master=scheduled_update)
    departure_time.grid(row=4, column=1)
    tk.Label(master=scheduled_update, bg="#1c1c1c",text="").grid(row=5, column=1)
    tk.Label(master=scheduled_update,bg="#1c1c1c", fg= "#fafaff",font="ubuntu", text="Enter Status:").grid(row=6, column=0)
    stat = tk.Entry(master=scheduled_update)
    stat.grid(row=6, column=1)
    tk.Label(master=scheduled_update, bg="#1c1c1c",text="").grid(row=7, column=1)
    tk.Label(master=scheduled_update,bg="#1c1c1c", fg= "#fafaff",font="ubuntu", text="Enter Destination:").grid(row=8, column=0)
    destination_place = tk.Entry(master=scheduled_update)
    destination_place.grid(row=8, column=1)
    tk.Label(master=scheduled_update, bg="#1c1c1c",text="").grid(row=9, column=1)
    tk.Button(master=scheduled_update, text="Confirm", command=update_btn1).grid(row=10, column=1)
    tk.Label(master=scheduled_update, bg="#1c1c1c",text="").grid(row=11, column=1)
       

def cancel():  # this function cancels flights
    def back_cancelled():
        flight = flight_number.get()
        cancelled_scheduled.destroy()
        if flight in cancelled:
            root = tk.Tk()
            root.title("Already Cancelled!")
            root['background']='#1c1c1c'
            tk.Label(master=root, bg="#1c1c1c",text="").grid(row=0, column=1)
            tk.Label(master=root, bg="#1c1c1c", fg= "#fafaff",font="ubuntu", text="Flight Already Cancelled. Please try again!").grid(row=1, column=1)
            tk.Label(master=root, bg="#1c1c1c",text="").grid(row=2, column=1)
        elif not (flight in scheduled):
            root = tk.Tk()
            root.title("Flight Not Found!")
            root['background']='#1c1c1c'
            tk.Label(master=root, bg="#1c1c1c",text="").grid(row=0, column=1)
            tk.Label(master=root, bg="#1c1c1c", fg= "#fafaff",font="ubuntu",  text="Flight Not Found. Please try again!").grid(row=1, column=1)
            tk.Label(master=root, bg="#1c1c1c",text="").grid(row=2, column=1)
        else:
            cursor.execute("update flights set status='CANCELLED' where flightno='%s'"%(flight))
            root = tk.Tk()
            root.title("Flight Cancelled!")
            root['background']='#1c1c1c'
            tk.Label(master=root, bg="#1c1c1c",text="").grid(row=0, column=1)
            tk.Label(master=root, bg="#1c1c1c", 
            
            
            fg= "#fafaff",font="ubuntu",  text="Flight Cancelled!").grid(row=1, column=1)
            tk.Label(master=root, bg="#1c1c1c",text="").grid(row=2, column=1)
            sync()

    cancelled_scheduled = tk.Tk()
    cancelled_scheduled.title("Cancel a Flight")
    cancelled_scheduled['background']='#1c1c1c'
    tk.Label(master=cancelled_scheduled, bg="#1c1c1c",text="").grid(row=1, column=1)
    tk.Label(master=cancelled_scheduled,bg="#1c1c1c", fg= "#fafaff",font="ubuntu", text="Enter the flight number:  ").grid(row=2, column=0)
    flight_number = tk.Entry(master=cancelled_scheduled)
    flight_number.grid(row=2, column=1)
    admin7 = tk.Button(master=cancelled_scheduled, width=18, text="Confirm", command=back_cancelled).grid(row=3,column=1)
    tk.Label(master=cancelled_scheduled, bg="#1c1c1c",text="").grid(row=4, column=1)

def admin_main_features():  # admin control panel
    def switch_users_admin():
        admin_main_scheduled.destroy()
        login()

    admin_main_scheduled = tk.Tk()
    admin_main_scheduled.title("Admin Control Panel")
    admin_main_scheduled['background']='#1c1c1c'
    tk.Label(master=admin_main_scheduled, bg="#1c1c1c",text="").grid(row=1, column=1)
    img = tk.PhotoImage(file="admin.png")
    no = tk.Label(master=admin_main_scheduled, image=img,borderwidth=0).grid(row=2, column=0)
    tk.Label(master=admin_main_scheduled, bg="#1c1c1c",text="").grid(row=3, column=1)
    tk.Button(master=admin_main_scheduled, text="View The Details Of Flights", width=25, command=viewing_flights).grid(row=4,column=0)
    tk.Label(master=admin_main_scheduled, bg="#1c1c1c",text="").grid(row=5, column=1)
    tk.Button(master=admin_main_scheduled, text="Switch User", width=25, command=switch_users_admin).grid(row=12, column=0)
    tk.Label(master=admin_main_scheduled, bg="#1c1c1c",text="").grid(row=7, column=1)
    tk.Button(master=admin_main_scheduled, text="Cancel A Flight", width=25, command=cancel).grid(row=8, column=0)
    tk.Label(master=admin_main_scheduled, bg="#1c1c1c",text="").grid(row=9, column=1)
    tk.Button(master=admin_main_scheduled, text="Display Users", width=25, command=display_users).grid(row=10, column=0)
    tk.Label(master=admin_main_scheduled, bg="#1c1c1c",text="").grid(row=11, column=1)
    tk.Button(master=admin_main_scheduled, text="Exit The Program", width=25, command=exit).grid(row=14, column=0)
    tk.Label(master=admin_main_scheduled, bg="#1c1c1c",text="").grid(row=13, column=1)
    tk.Button(master=admin_main_scheduled, text="Update/Add A Flight", width=25, command=update).grid(row=6, column=0)
    tk.Label(master=admin_main_scheduled, bg="#1c1c1c",text="").grid(row=15, column=1)
    admin_main_scheduled.mainloop()

def book_flight():
    def book_btn1():
        destination=destination_book.get()
        cursor.execute("select * from flights where destination='%s'"%(destination))
        result=cursor.fetchall()
        scheduled_update.destroy()
        if len(result) == 0:
            update_root = tk.Tk()
            update_root.title("No Flights Found!")
            update_root['background']='#1c1c1c'
            tk.Label(master=update_root, bg="#1c1c1c",text="").grid(row=0, column=1)
            tk.Label(master=update_root, bg="#1c1c1c", fg= "#fafaff",font="ubuntu",text="No flights are flying to your desired desination.").grid(row=1, column=0)
            tk.Label(master=update_root, bg="#1c1c1c",text="").grid(row=2, column=1)
        else:
            can = 0
            ret = 2
            display = tk.Tk()
            display.title("Available Flights")
            display['background']='#1c1c1c'
            tk.Label(master=display, bg="#1c1c1c",text="").grid(row=0, column=1)
            tk.Label(master=display, bg="#1c1c1c", fg= "#fafaff",font="ubuntu",text="Flight Number--------Departure--------Destination-------Status").grid(row=1, column=0)
            tk.Label(master=display, bg="#1c1c1c",text="").grid(row=2, column=1)
            for i in result:
                can += 1
                ret += 1
                tk.Label(master=display, bg="#1c1c1c", fg= "#fafaff",
                         text=(i[0], "-------", i[1], "--------", i[2], "--------", i[3])).grid(row=ret, column=0)

    scheduled_update = tk.Tk()
    scheduled_update.title("Book A Flight")
    scheduled_update['background']='#1c1c1c'
    tk.Label(master=scheduled_update, bg="#1c1c1c",text="").grid(row=0, column=1)
    tk.Label(master=scheduled_update, bg="#1c1c1c", fg= "#fafaff",font="ubuntu", text="Enter Your Destination:   ").grid(row=1, column=0)
    destination_book = tk.Entry(master=scheduled_update)
    destination_book.grid(row=1, column=1)
    tk.Label(master=scheduled_update, bg="#1c1c1c",text="").grid(row=2, column=1)
    tk.Button(master=scheduled_update, text="Confirm", command=book_btn1).grid(row=3, column=1)
    tk.Label(master=scheduled_update, bg="#1c1c1c",text="").grid(row=4, column=1)
       

def viewing_flights():  # viewing flights
    can = 0
    ret = 3
    display = tk.Tk()
    display.title("View Details Of Flights")
    display['background']='#1c1c1c'
    tk.Label(master=display,bg="#1c1c1c", text="").grid(row=1, column=1)
    tk.Label(master=display,bg="#1c1c1c", fg= "#fafaff",font="ubuntu", text="Flight Number--------Departure--------Destination-------Status").grid(row=2, column=0)
    tk.Label(master=display,bg="#1c1c1c", text="").grid(row=3, column=1)
    for i in scheduled:
        can += 1
        ret += 1
        tk.Label(master=display,bg="#1c1c1c", fg= "#fafaff",
                 text=(i, "-------", scheduled[i][0], "--------", scheduled[i][1], "--------", scheduled[i][2])).grid(
            row=ret, column=0)
    for i in cancelled:
        can += 1
        ret += 1
        tk.Label(master=display,bg="#1c1c1c", fg= "#fafaff",
                 text=(i, "-------", cancelled[i][0], "--------", cancelled[i][1], "--------", cancelled[i][2])).grid(
            row=ret, column=0)


def main_standard():  # standard user control panel
    def switch_user_standard():
        main_standard_scheduled.destroy()
        login()

    main_standard_scheduled = tk.Tk()
    main_standard_scheduled.title("Standard User Control Panel")

    main_standard_scheduled['background']='#1c1c1c'
    tk.Label(master=main_standard_scheduled, bg="#1c1c1c",text="").grid(row=0, column=1)
    img = tk.PhotoImage(file="user.png")
    no = tk.Label(master=main_standard_scheduled, image=img,borderwidth=0).grid(row=1, column=0)
    tk.Label(master=main_standard_scheduled, bg="#1c1c1c",text="").grid(row=2, column=1)
    tk.Button(master=main_standard_scheduled, text="View The Details Of Flights",width=25, command=viewing_flights).grid(row=3,column=0)
    tk.Label(master=main_standard_scheduled, bg="#1c1c1c",text="").grid(row=4, column=1)
    tk.Button(master=main_standard_scheduled, text="Book Flight",width=25, command=book_flight).grid(row=5, column=0)
    tk.Label(master=main_standard_scheduled, bg="#1c1c1c",text="").grid(row=6, column=1)
    tk.Button(master=main_standard_scheduled, text="Switch User",width=25,command=switch_user_standard).grid(row=7, column=0)
    tk.Label(master=main_standard_scheduled, bg="#1c1c1c",text="").grid(row=8, column=1)
    tk.Button(master=main_standard_scheduled, text="Exit The Program",width=25, command=exit).grid(row=9, column=0)
    tk.Label(master=main_standard_scheduled, bg="#1c1c1c",text="").grid(row=10, column=1)    
    main_standard_scheduled.mainloop()

def login():
    def user_verification():
        def password_verification():
            pas = password.get()
            if check == 1:
                if admin[a] == pas:
                    login_sched.destroy()
                    admin_main_features()
                else:
                    admin3 = tk.Tk()
                    admin3.title("Wrong Password!")
                    tk.Label(master=admin3, text="Wrong Password! Please Try Again!").grid(row=1, column=1)

            elif check == 2:
                if standard[a] == pas:
                    login_sched.destroy()
                    main_standard()

                else:
                    admin3 = tk.Tk()
                    admin3.title("Wrong Password!")
                    tk.Label(master=admin3, text="Wrong Password! Please Try Again!").grid(row=1, column=1)

        a = username.get()

        if not (a in admin or  a in standard):
            admin1 = tk.Tk()
            admin1.title("Wrong Username!")
            tk.Label(master=admin1, text="Username Not Found. Please Try Again!").grid(row=1, column=1)
        else:
            if a in admin:
                check = 1
            elif a in standard:
                check = 2

            tk.Label(master=login_sched,bg="#1c1c1c", fg= "#fafaff",font="ubuntu", text="     Enter Your Password").grid(row=6, column=0)
            password = tk.Entry(master=login_sched, show='*')
            password.grid(row=6, column=1)
            admin3 = tk.Button(master=login_sched, text="Confirm Password", width=25, command=password_verification).grid(row=6, column=2)
            tk.Label(master=login_sched,bg="#1c1c1c", text="").grid(row=7, column=1)

    login_sched = tk.Tk()
    login_sched.title("Login")
    login_sched['background']='#1c1c1c'
    tk.Label(master=login_sched, bg="#1c1c1c",text="").grid(row=1, column=1)
    image = tk.PhotoImage(file="signin.png")
    no = tk.Label(master=login_sched, image=image,borderwidth=0).grid(row=2, column=1)
    tk.Label(master=login_sched, bg="#1c1c1c",text="").grid(row=3, column=1)
    tk.Label(master=login_sched, bg="#1c1c1c", fg= "#fafaff",font="ubuntu",text="     Enter Your Username").grid(row=4, column=0)
    username = tk.Entry(master=login_sched)
    username.grid(row=4, column=1)
    asking = tk.Button(master=login_sched, text="Confirm Username", width=25, command=user_verification).grid(row=4,column=2)
    tk.Label(master=login_sched,bg="#1c1c1c", text="").grid(row=5, column=1)
    login_sched.mainloop()

sync()
login()