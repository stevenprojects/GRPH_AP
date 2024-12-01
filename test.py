def read_integer_between_numbers(prompt, mini, maximum):
    while True:
        try:
            users_input = int(input(prompt))
            if mini <= users_input <= maximum:
                return users_input
            else:
                print(f"Numbers from {mini} to {maximum} only.")
        except ValueError:
            print("Sorry - number only please.")


def read_nonempty_string(prompt):
    while True:
        users_input = input(prompt)
        if len(users_input) > 0 and users_input.isalpha():
            return users_input
        print("Please enter a non-empty alphabetical string.")


def read_integer(prompt):
    while True:
        try:
            users_input = int(input(prompt))
            if users_input >= 0:
                return users_input
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Sorry - number only please.")


def runners_data():
    with open("runners.txt") as input_file:
        lines = input_file.readlines()
    runners_name = []
    runners_id = []
    for line in lines:
        split_line = line.strip().split(",")
        if len(split_line) >= 2:  # Ensure valid format
            runners_name.append(split_line[0])
            runners_id.append(split_line[1])
    return runners_name, runners_id


def race_venues():
    with open("races.txt") as input_file:
        lines = input_file.readlines()
    # Extract only the venue names (before the comma)
    races_location = [line.split(",")[0].strip() for line in lines]
    return races_location


def reading_race_results(location):
    try:
        with open(f"{location}.txt") as input_file:
            lines = input_file.readlines()
        id = []
        time_taken = []
        for line in lines:
            split_line = line.strip().split(",")
            if len(split_line) >= 2:  # Ensure valid format
                id.append(split_line[0])
                time_taken.append(int(split_line[1]))
        return id, time_taken
    except FileNotFoundError:
        print(f"Error: No file found for race venue '{location}'.")
        return [], []


def winner_of_race(id, time_taken):
    sorted_times = sorted(zip(time_taken, id))
    return [runner[1] for runner in sorted_times[:3]]  # Top 3


def display_races(id, time_taken, venue, podium):
    MINUTE = 60
    print(f"Results for {venue}")
    print("=" * 37)
    for i in range(len(id)):
        minutes = time_taken[i] // MINUTE
        seconds = time_taken[i] % MINUTE
        print(f"{id[i]:<10s} {minutes} minutes and {seconds} seconds")
    print("\nPodium Places:")
    print(f"1st: {podium[0]}")
    print(f"2nd: {podium[1]}")
    print(f"3rd: {podium[2]}")


def users_venue(races_location, runners_id):
    while True:
        user_location = read_nonempty_string("Where will the new race take place? ").capitalize()
        if user_location not in races_location:
            break
    with open(f"{user_location}.txt", "w") as connection:
        races_location.append(user_location)
        for runner_id in runners_id:
            time_taken_for_runner = read_integer(f"Time for {runner_id} (in seconds, or 0 if not participated) >> ")
            print(f"{runner_id},{time_taken_for_runner}", file=connection)


def updating_races_file(races_location):
    with open("races.txt", "w") as connection:
        for race in races_location:
            print(race, file=connection)


def competitors_by_county(name, id):
    counties = {}
    for i in range(len(id)):
        county_code = id[i].split("-")[0]
        if county_code not in counties:
            counties[county_code] = []
        counties[county_code].append(f"{name[i]} ({id[i]})")
    for county, competitors in sorted(counties.items()):
        print(f"{county} runners")
        print("=" * 20)
        for competitor in sorted(competitors):
            print(competitor)
        print()


def display_podium_places(races_location):
    print(f"{'Venue':<20}{'1st':<10}{'2nd':<10}{'3rd':<10}")
    print("=" * 50)
    for venue in races_location:
        id, time_taken = reading_race_results(venue)
        if id and time_taken:  # Ensure data exists for the race
            podium = winner_of_race(id, time_taken)
            print(f"{venue:<20}{podium[0]:<10}{podium[1]:<10}{podium[2]:<10}")


def display_race_times_one_competitor(races_location, runner_id):
    print(f"Results for {runner_id}")
    print("-" * 40)
    for venue in races_location:
        id, time_taken = reading_race_results(venue)
        if runner_id in id:
            index = id.index(runner_id)
            minutes = time_taken[index] // 60
            seconds = time_taken[index] % 60
            position = sorted(zip(time_taken, id)).index((time_taken[index], runner_id)) + 1
            print(f"{venue:<15} {minutes} mins {seconds} secs (Position: {position})")


def show_winners(races_location, runners_name, runners_id):
    winners = set()
    for venue in races_location:
        id, time_taken = reading_race_results(venue)
        if id and time_taken:  # Ensure data exists
            winners.add(winner_of_race(id, time_taken)[0])  # Add 1st place
    print("Runners who have won at least one race:")
    for i, runner_id in enumerate(runners_id):
        if runner_id in winners:
            print(f"{runners_name[i]} ({runner_id})")


def show_non_podium_runners(races_location, runners_name, runners_id):
    podium_runners = set()
    for venue in races_location:
        id, time_taken = reading_race_results(venue)
        if id and time_taken:  # Ensure data exists
            podium = winner_of_race(id, time_taken)
            podium_runners.update(podium)
    print("Runners who have not taken a podium position in any race:")
    for i, runner_id in enumerate(runners_id):
        if runner_id not in podium_runners:
            print(f"{runners_name[i]} ({runner_id})")


def main():
    races_location = race_venues()
    runners_name, runners_id = runners_data()
    MENU = (
        "1. Show the results for a race\n"
        "2. Add results for a race\n"
        "3. Show all competitors by county\n"
        "4. Display the podium-places of each race\n"
        "5. Display all the race times for one competitor\n"
        "6. Show all competitors who have won a race\n"
        "7. Show all competitors who have not taken a podium-position in any race\n"
        "8. Quit\n>>> "
    )
    while True:
        input_menu = read_integer_between_numbers(MENU, 1, 8)
        if input_menu == 1:
            for i, venue in enumerate(races_location, start=1):
                print(f"{i}. {venue}")
            choice = read_integer_between_numbers("Select a race: ", 1, len(races_location))
            venue = races_location[choice - 1]
            id, time_taken = reading_race_results(venue)
            if id and time_taken:
                podium = winner_of_race(id, time_taken)
                display_races(id, time_taken, venue, podium)
            else:
                print(f"No results found for {venue}.")
        elif input_menu == 2:
            users_venue(races_location, runners_id)
        elif input_menu == 3:
            competitors_by_county(runners_name, runners_id)
        elif input_menu == 4:
            display_podium_places(races_location)
        elif input_menu == 5:
            for i, name in enumerate(runners_name, start=1):
                print(f"{i}. {name}")
            choice = read_integer_between_numbers("Select a runner: ", 1, len(runners_name))
            runner_id = runners_id[choice - 1]
            display_race_times_one_competitor(races_location, runner_id)
        elif input_menu == 6:
            show_winners(races_location, runners_name, runners_id)
        elif input_menu == 7:
            show_non_podium_runners(races_location, runners_name, runners_id)
        elif input_menu == 8:
            updating_races_file(races_location)
            break


if __name__ == "__main__":
    main()
