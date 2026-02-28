import serial
from typing import Optional, Tuple
import math

import logwrite
import config


class GPSModule:
    def __init__(self, port: str = None, baud_rate: int = None):

        # ===== config優先 =====
        self.port = port if port else getattr(config, "GPS_PORT", "/dev/serial0")
        self.baud_rate = baud_rate if baud_rate else getattr(config, "GPS_BAUDRATE", 9600)

        self.serial_connection = None
        self.log = logwrite.MyLogging()

    def connect(self):
        try:
            self.serial_connection = serial.Serial(
                self.port,
                self.baud_rate,
                timeout=1
            )
            self.log.write(f"GPS connected: {self.port}", "INFO")

        except Exception as e:
            self.log.write("Failed to connect to GPS module", "ERROR")
            raise ConnectionError(f"Failed to connect to GPS module: {e}")

    def disconnect(self):
        if self.serial_connection:
            self.serial_connection.close()
            self.log.write("GPS module disconnected.", "INFO")

    def parse_nmea_sentence(
        self, sentence: str
    ) -> Tuple[Optional[float], Optional[float], Optional[int], Optional[str], Optional[float]]:

        try:
            parts = sentence.split(',')

            if parts[0] == "$GPGGA":

                utc_time = parts[1][:6]

                raw_lat = parts[2]
                lat_dir = parts[3]
                raw_lon = parts[4]
                lon_dir = parts[5]

                satellite_count = int(parts[7]) if parts[7].isdigit() else None

                # ===== DOPをfloatに =====
                dop = float(parts[8]) if parts[8] else None

                lat = float(raw_lat[:2]) + float(raw_lat[2:]) / 60.0 if raw_lat else None
                if lat_dir == "S":
                    lat = -lat

                lon = float(raw_lon[:3]) + float(raw_lon[3:]) / 60.0 if raw_lon else None
                if lon_dir == "W":
                    lon = -lon

                return lat, lon, satellite_count, utc_time, dop

        except (ValueError, IndexError):
            pass

        return None, None, None, None, None

    def get_gps_data(self):

        if not self.serial_connection:
            self.log.write("GPS not connected", "ERROR")
            raise ConnectionError("GPS module is not connected.")

        try:
            while True:
                line = (
                    self.serial_connection.readline()
                    .decode("ascii", errors="replace")
                    .strip()
                )

                if line.startswith("$GPGGA"):
                    return self.parse_nmea_sentence(line)

                self.serial_connection.reset_input_buffer()

        except Exception as e:
            self.log.write(f"GPS read error: {e}", "ERROR")

        return None, None, None, None, None


def calculate_target_distance_angle(
    current_coordinate,
    previous_coordinate,
    goal_coordinate,
    TARGET_DISTANCE,
):

    log = logwrite.MyLogging()

    coordinate_diff_goal = {
        "lat": goal_coordinate["lat"] - current_coordinate["lat"],
        "lon": goal_coordinate["lon"] - current_coordinate["lon"],
    }

    degree_for_goal = math.atan2(
        coordinate_diff_goal["lon"],
        coordinate_diff_goal["lat"],
    ) / math.pi * 180

    log.write(f"degree_for_goal:{degree_for_goal}", "DEBUG")

    coordinate_diff_me = {
        "lat": current_coordinate["lat"] - previous_coordinate["lat"],
        "lon": current_coordinate["lon"] - previous_coordinate["lon"],
    }

    degree_for_me = math.atan2(
        coordinate_diff_me["lon"],
        coordinate_diff_me["lat"],
    ) / math.pi * 180

    log.write(f"degree_for_me:{degree_for_me}", "DEBUG")

    log.forLATLON(degree_for_goal, degree_for_me)

    degree = degree_for_goal - degree_for_me

    if degree < -180:
        degree += 360
    elif degree > 180:
        degree -= 360

    distance = (
        math.sqrt(
            coordinate_diff_goal["lat"] ** 2 +
            coordinate_diff_goal["lon"] ** 2
        )
        * 10**5
    )

    if distance <= TARGET_DISTANCE:
        return {"dir": "Immediate", "deg": 0, "distance": distance}

    if degree <= -45:
        return {"dir": "left", "deg": degree, "distance": distance}
    elif degree >= 45:
        return {"dir": "right", "deg": degree, "distance": distance}
    else:
        return {"dir": "forward", "deg": degree, "distance": distance}

if __name__ == "__main__":
    gps = GPSModule()
    #log = logwrite.MyLogging()
    try:
        gps.connect()
        print("Fetching GPS data...")
        while True:
            try:
                lat, lon, satellites, utc_time, dop = gps.get_gps_data()
                if lat is not None and lon is not None:
                    #log.write(f"Latitude: {lat:.6f}, Longitude: {lon:.6f}, Satellites: {satellites}, Time: {utc_time}, DOP: {dop}","INFO")
                    print(f"Latitude: {lat:.6f}, Longitude: {lon:.6f}, Satellites: {satellites}, Time: {utc_time}, DOP: {dop}","INFO")
                    #logwrite.forCSV(lat,lon)
                    pass
                    # ロギングを追加する場合、以下に記述
                # Example: log_to_file(lat, lon, satellites, time_utc, dop)
                else:
                    print("Waiting")
                    #logwrite.forCSV(lat,lon)
            except KeyboardInterrupt:
                break
            except Exception as e:
                #log.write(e,"CRITICAL")
                print(e)
    except KeyboardInterrupt:
        print("Terminating program.")
    except Exception as e :
        #log.write(e,"ERROR")
        print(e)
    finally:
        gps.disconnect()
