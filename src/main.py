from planner import DeskPlanner 
#set up steps needed

#how to interact w robot? 
#when to error/ try accept, good code writing? 
#do i need helper functions? what helper functions do I need? 

#break into parts and test part by part 
#main loop 
#run perception, trash and human 
#listen for voice 
#input perception and voice into planner 
#planner outputs action word
#policy or skill chosen by planner 
#action ran through saftey 
#action happens 


def main():

    #project_root = find_project_root()
    #print(f"Project root: {project_root}")

    #robot = None

    #chat given try and clean up code, fix to match how to intereact w interface 
    try:
        print("Loading robot...")
        robot = load_robot()

        print("Connecting robot...")
        robot.connect()
        print("Robot connected.")

        print("Loading policy...")
        policy = load_policy()
        print("Policy loaded.")

        run_policy_loop(
            robot=robot,
            policy=policy,
            num_steps=NUM_STEPS,
            control_dt=CONTROL_DT,
        )

    except KeyboardInterrupt:
        print("Stopped by user with Ctrl+C.")

    except Exception as error:
        print(f"Error: {error}")

    finally:
        print("Cleaning up...")

        if robot is not None:
            try:
                # Some LeRobot versions have disconnect().
                robot.disconnect()
                print("Robot disconnected.")
            except AttributeError:
                print("robot.disconnect() not available in this LeRobot version.")
            except Exception as error:
                print(f"Error while disconnecting robot: {error}")

        print("Done.")


if __name__ == "__main__":
    main()

