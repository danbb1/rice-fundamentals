"""
Cookie Clicker Simulator
"""
import math
import poc_clicker_provided as provided
import simpleplot
#import poc_simpletest
# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)


# Constants
SIM_TIME = 200.0


class ClickerState:
    """
    Simple class to keep track of the game state.
    """

    def __init__(self):
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._current_time = 0.0
        self._current_CPS = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]

    def __str__(self):
        """
        Return human readable state
        """
        return "\nTotal Cookies: " + str(self._total_cookies) + "\nCurrent Cookies: " + str(self.get_cookies()) + "\nCurrent Time: " + str(self.get_time()) + "\nCurrent CPS: " + str(self.get_cps()) + "\n"

    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)

        Should return a float
        """
        return self._current_cookies

    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_CPS

    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time

    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        clone_history = list(self._history)
        return clone_history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        time_until = float(math.ceil((cookies - self.get_cookies()) / self.get_cps()))
        
        return time_until if time_until >= 0.0 else 0.0 

    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time <= 0.0:
            return

        self._current_time += time
        self._current_cookies += (time * self.get_cps())
        self._total_cookies += (time * self.get_cps())

    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if cost > self.get_cookies():
            return

        new_item = (self.get_time(), item_name, cost, self._total_cookies)
        
        self._history.append(new_item)
        self._current_cookies -= cost
        self._current_CPS += additional_cps


def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """

    # Replace with your code
    clone_build_info = build_info.clone()
    new_game = ClickerState()

    while new_game.get_time() <= duration:
        current_time = new_game.get_time()
        current_cookies = new_game.get_cookies()
        current_cps = new_game.get_cps()
        
        #print "In the loop at time:", current_time
        #print new_game
        if current_time > duration:
          break
        next_item = strategy(current_cookies, current_cps, new_game.get_history(), duration - current_time, clone_build_info)
        
        if next_item == None:
          new_game.wait(duration - current_time)
          break
          
        next_item_cost = clone_build_info.get_cost(next_item)
        time_until_next_item = new_game.time_until(next_item_cost)
        
        #print "Want to buy a ", next_item, "Which costs", next_item_cost, "Will have to wait", time_until_next_item
        
        if current_time == duration and next_item_cost == current_cookies:
            new_game.buy_item(next_item, next_item_cost, clone_build_info.get_cps(next_item))
            clone_build_info.update_item(next_item)
            break
        
        if time_until_next_item + current_time > duration:
          #print "No time."
          new_game.wait(duration - current_time)
          break
        elif time_until_next_item == 0.0:
          new_game.buy_item(next_item, next_item_cost, clone_build_info.get_cps(next_item))
          clone_build_info.update_item(next_item)
          #print "Bought the item!"
        else:
          #print "waiting..."
          new_game.wait(time_until_next_item)
    return new_game

def sort_items_cost_ascending(build_info):
    """
    Sorts build items by cost ascending into a list of tuples of form (name, cost, cps)
    """
    items = build_info.build_items()
    
    dict_items = {}
    
    for item in items:
      dict_items.update({ item: build_info.get_cost(item) })
    
    sorted_items = sorted(dict_items.items(), key=lambda x:x[1])
    
    for index, item in enumerate(sorted_items):
        sorted_items[index] = item + (build_info.get_cps(item[0]),)
    
    return sorted_items


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"


def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None


def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    build_items = build_info.build_items()
    cheapest = build_items[0]
    
    for item in build_items:
      if build_info.get_cost(item) < build_info.get_cost(cheapest):
        cheapest = item
      
    return cheapest if cookies + (cps * time_left) >= build_info.get_cost(cheapest) else None


def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    #set the most expensive item with enough time left to buy
    sorted_build_items = sort_items_cost_ascending(build_info)
    most_expensive = sorted_build_items[0]
    
    for item in sorted_build_items:
      if item[1] > most_expensive[1] and cookies + (cps * time_left) >= item[1]:
        most_expensive = item
            
    return most_expensive[0] if cookies + (cps * time_left) >= most_expensive[1] else None

    return None

def time_until(cost, current_cookies, cps):
    time_until = float(math.ceil((cost - current_cookies) / cps))
    
    return time_until if time_until > 0.0 else 0.0

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    sorted_build_items = sort_items_cost_ascending(build_info)
    
    next_item = sorted_build_items[0]
    
    for item in sorted_build_items:
        
        if (item[2] / item[1]) > (next_item[2] / next_item[1]) and cookies + (cps * time_left) >= item[1]:
            next_item = item
            
    return next_item[0] if cookies + (cps * time_left) >= next_item[1] else None


def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)


def run():
    """
    Run the simulator.
    """
    #run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    

#run()


# def clickerstate_test_suite():
#     suite = poc_simpletest.TestSuite()

#     print "Running clickerstate test suite"

#     new_game = ClickerState()

#     def reset():
#         new_game.total_cookies = 0.0
#         new_game.current_cookies = 0.0
#         new_game.current_time = 0.0
#         new_game.current_CPS = 1.0
#         new_game.history = [(0.0, None, 0.0, 0.0)]

#     print "Testing state initialises with correct values"
#     suite.run_test(new_game.get_cookies(), 0.0, "Get Cookies")
#     suite.run_test(new_game.get_cps(), 1.0, "Get CPS")
#     suite.run_test(new_game.get_time(), 0.0, "Get Time")
#     suite.run_test(new_game.total_cookies, 0.0, "Total Cookies")
#     suite.run_test(new_game.get_history(), [
#                    (0.0, None, 0.0, 0.0)], "Get History")

#     print "Testing Time Until"
#     suite.run_test(isinstance(new_game.time_until(100), float),
#                    True, "Is a float")
#     suite.run_test(new_game.time_until(100), 100.0, "#1")
#     new_game.current_CPS = 2
#     suite.run_test(new_game.time_until(100), 50.0, "#2")
#     new_game.current_cookies = 50
#     suite.run_test(new_game.time_until(100), 25.0, "#3")
#     reset()
#     new_game.current_cookies = 1000
#     new_game.current_CPS = 2.5
#     suite.run_test(new_game.time_until(2000), 400.0, "#4")
#     reset()
#     new_game.current_cookies = 100
#     suite.run_test(new_game.time_until(100), 0.0, "#5")
#     new_game.current_CPS = 1.3
#     suite.run_test(new_game.time_until(120), 16.0, "#6")

#     reset()

#     print "Testing Wait"
#     new_game.wait(100)
#     suite.run_test(new_game.get_cookies(), 100.0, "#1")
#     suite.run_test(new_game.get_time(), 100.0, "#1")
#     suite.run_test(new_game.total_cookies, 100.0, "#3")
#     new_game.current_cookies = 0.0
#     new_game.wait(200)
#     suite.run_test(new_game.get_cookies(), 200.0, "#1")
#     suite.run_test(new_game.get_time(), 300.0, "#1")
#     suite.run_test(new_game.total_cookies, 300.0, "#3")
#     new_game.wait(0)
#     suite.run_test(new_game.total_cookies, 300.0, "#3")
#     new_game.wait(-10)
#     suite.run_test(new_game.total_cookies, 300.0, "#3")

#     reset()

#     print "Testing Buy Item"
#     new_game.buy_item("Too Expensive", 1000, 3.0)
#     suite.run_test(new_game.get_history(), [(0.0, None, 0.0, 0.0)], "#1")
#     new_game.wait(1000)
#     new_game.buy_item("Affordable", 500.0, 1.0)
#     suite.run_test(new_game.get_history(), [
#                    (0.0, None, 0.0, 0.0), (1000.0, "Affordable", 500.0, 1000.0)], "#2")
#     suite.run_test(new_game.get_cookies(), 500.0, "#3")
#     suite.run_test(new_game.total_cookies, 1000.0, "#4")
#     suite.run_test(new_game.get_cps(), 2.0, "#5")
#     new_game.wait(1000)
#     new_game.buy_item("Affordable", 500.0, 1.0)
#     suite.run_test(new_game.get_history(), [(0.0, None, 0.0, 0.0), (
#         1000.0, "Affordable", 500.0, 1000.0), (2000.0, "Affordable", 500.0, 3000.0)], "#6")
#     suite.run_test(new_game.get_cookies(), 2000.0, "#7")
#     suite.run_test(new_game.total_cookies, 3000.0, "#8")
#     suite.run_test(new_game.get_cps(), 3.0, "#8")
#     new_game.buy_item("No Way", 1000000.0, 10.0)
#     suite.run_test(new_game.get_history(), [(0.0, None, 0.0, 0.0), (
#         1000.0, "Affordable", 500.0, 1000.0), (2000.0, "Affordable", 500.0, 3000.0)], "#9")
#     suite.run_test(new_game.get_cookies(), 2000.0, "#10")
#     suite.run_test(new_game.total_cookies, 3000.0, "#11")
#     suite.run_test(new_game.get_cps(), 3.0, "#12")
    
#     reset()
    
#     new_game.wait(78)
#     new_game.buy_item('item', 1.0, 1.0)
#     suite.run_test(new_game.time_until(22), 0.0, "Test")


#     suite.report_results()


# clickerstate_test_suite()
