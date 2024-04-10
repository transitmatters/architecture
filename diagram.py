from charts.full import full
from charts.simplified import simplified
from charts.new_train_tracker import new_train_tracker
from charts.mbta_covid_recovery_dashboard import mbta_covid_recovery_dash
from charts.regional_rail_explorer import regional_rail_explorer
from charts.mbta_slow_zone_bot import mbta_slow_zone_bot
from charts.data_dashboard import data_dashboard

if __name__ == "__main__":
    full()
    simplified()
    new_train_tracker()
    mbta_covid_recovery_dash()
    regional_rail_explorer()
    mbta_slow_zone_bot()
    data_dashboard()
