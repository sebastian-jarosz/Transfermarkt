import os
import Scripts.Other.transfermarkt_app_constants as const

from sys import platform


def get_platform_attributes():
    if platform == const.MAC[const.KEY_PLATFORM]:
        used_platform = const.MAC
    elif platform == const.WINDOWS[const.KEY_PLATFORM]:
        used_platform = const.WINDOWS
    else:
        return

    return used_platform


def get_main_export_dir_path():
    used_platform = get_platform_attributes()
    dir_names = [os.environ[used_platform[const.KEY_HOME_DIR]]]

    for directory in const.EXPORT_PATH_DIRS:
        dir_names.append(directory)

    main_export_path = used_platform[const.KEY_DELIMITER].join(dir_names)

    return main_export_path


def get_season_dir_export_path(country_name, league_name, season):
    used_platform = get_platform_attributes()
    main_export_dir_path = get_main_export_dir_path()

    dir_array = [main_export_dir_path, country_name, league_name, str(season)]
    season_dir_path = used_platform[const.KEY_DELIMITER].join(dir_array)

    return season_dir_path


def get_season_players_file_path(country_name, league_name, season):
    season_players_file_path = get_season_dir_export_path(country_name, league_name, season)
    return season_players_file_path + const.PLAYERS_FILE_NAME


def create_season_directory(country_name, league_name, season):
    season_dir_path = get_season_dir_export_path(country_name, league_name, season)

    if not os.path.exists(season_dir_path):
        os.makedirs(season_dir_path)
        print("Directory created successfully: " + season_dir_path)
    else:
        print("Directory exists: " + season_dir_path)
