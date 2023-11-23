

 # OrderMonitor.py
# Copyright 2019 Gehtsoft USA LLC

# Licensed under the license derived from the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License.

# You may obtain a copy of the License at

# http://fxcodebase.com/licenses/open-source/license.html

# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List
from enum import Enum
import json
import os

try:
    # Try to import fxcorepy from forexconnect
    from forexconnect import fxcorepy
except ModuleNotFoundError:
    # If that fails, try to import fxcorepy directly
    try:
        from .forexconnect import fxcorepy
    except ModuleNotFoundError:
        # If that also fails, print an error message
        print("Could not import fxcorepy. Please ensure the module is installed and available.")


class OrderMonitor:
    class ExecutionResult(Enum):
        EXECUTING = 1
        EXECUTED = 2
        PARTIAL_REJECTED = 3
        FULLY_REJECTED = 4
        CANCELED = 5

    class OrderState(Enum):
        ORDER_EXECUTING = 1
        ORDER_EXECUTED = 2
        ORDER_CANCELED = 3
        ORDER_REJECTED = 4

    __market_condition = "5"

    def __init__(self, order: fxcorepy.O2GOrderRow) -> None:
        self.__order = order
        self.__trades = []
        self.__closed_trades = []
        self.__state = OrderMonitor.OrderState.ORDER_EXECUTING
        self.__result = OrderMonitor.ExecutionResult.EXECUTING
        self.__total_amount = 0
        self.__reject_amount = 0
        self.__reject_message = ""

    @staticmethod
    def is_opening_order(order: fxcorepy.O2GOrderRow) -> bool:
        return order.type.startswith("O")

    @staticmethod
    def is_closing_order(order: fxcorepy.O2GOrderRow) -> bool:
        return order.type.startswith("C")

    @property
    def order_row(self) -> fxcorepy.O2GOrderRow:
        return self.__order

    @property
    def trade_rows(self) -> List[fxcorepy.O2GTradeRow]:
        return self.__trades

    @property
    def closed_trade_rows(self) -> List[fxcorepy.O2GClosedTradeRow]:
        return self.__closed_trades

    @property
    def reject_amount(self) -> int:
        return self.__reject_amount

    @property
    def reject_message(self) -> str:
        return self.__reject_message

    @property
    def result(self) -> ExecutionResult:
        return self.__result

    @property
    def is_order_completed(self) -> bool:
        print(self.__result)
        return self.__result != OrderMonitor.ExecutionResult.EXECUTING

    @property
    def is_all_trades_received(self) -> bool:
        if self.__state == OrderMonitor.OrderState.ORDER_EXECUTING:
            return False
        i_current_total_amount = 0
        for trade in self.__trades:
            i_current_total_amount += trade.amount

        for trade in self.__closed_trades:
            i_current_total_amount += trade.amount

        return i_current_total_amount == self.__total_amount

    def on_trade_added(self, trade: fxcorepy.O2GTradeRow) -> None:
        trade_order_id = trade.open_order_id
        order_id = self.__order.order_id
        if trade_order_id == order_id:
            self.__trades.append(trade)
            if self.__state == OrderMonitor.OrderState.ORDER_EXECUTED or \
                    self.__state == OrderMonitor.OrderState.ORDER_REJECTED or \
                    self.__state == OrderMonitor.OrderState.ORDER_CANCELED:
                if self.is_all_trades_received:
                    self.set_result(True)

    def on_closed_trade_added(self, closed_trade: fxcorepy.O2GClosedTradeRow) -> None:
        order_id = self.__order.order_id
        closed_trade_order_id = closed_trade.close_order_id
        print(closed_trade_order_id, order_id)
        if order_id == closed_trade_order_id:
            self.__closed_trades.append(closed_trade)
            if self.__state == OrderMonitor.OrderState.ORDER_EXECUTED or \
                    self.__state == OrderMonitor.OrderState.ORDER_REJECTED or \
                    self.__state == OrderMonitor.OrderState.ORDER_CANCELED:
                if self.is_all_trades_received:
                    self.set_result(True)

    def on_order_deleted(self, order: fxcorepy.O2GOrderRow) -> None:
        deleted_order_id = order.order_id
        order_id = self.__order.order_id
        if deleted_order_id == order_id:
            # Store Reject amount
            if order.status.startswith("R"):
                self.__state = OrderMonitor.OrderState.ORDER_REJECTED
                self.__reject_amount = order.amount
                self.__total_amount = order.origin_amount - self.__reject_amount
                if self.__reject_message != "" and self.is_all_trades_received:
                    self.set_result(True)
            elif order.status.startswith("C"):
                self.__state = OrderMonitor.OrderState.ORDER_CANCELED
                self.__reject_amount = order.amount
                self.__total_amount = order.origin_amount - self.__reject_amount
                if self.is_all_trades_received:
                    self.set_result(False)
            else:
                self.__reject_amount = 0
                self.__total_amount = order.origin_amount
                self.__state = OrderMonitor.OrderState.ORDER_EXECUTED
                if self.is_all_trades_received:
                    self.set_result(True)

    def on_message_added(self, message: fxcorepy.O2GMessageRow) -> None:
        if self.__state == OrderMonitor.OrderState.ORDER_REJECTED or \
                self.__state == OrderMonitor.OrderState.ORDER_EXECUTING:
            is_reject_message = self.check_and_store_message(message)
            if self.__state == OrderMonitor.OrderState.ORDER_REJECTED and is_reject_message:
                self.set_result(True)

    def set_result(self, success: bool) -> None:
        if success:
            if self.__reject_amount == 0:
                self.__result = OrderMonitor.ExecutionResult.EXECUTED
            else:
                self.__result = OrderMonitor.ExecutionResult.FULLY_REJECTED \
                    if (len(self.__trades) == 0 and len(self.__closed_trades) == 0) \
                    else OrderMonitor.ExecutionResult.PARTIAL_REJECTED

        else:
            self.__result = OrderMonitor.ExecutionResult.CANCELED

    def check_and_store_message(self, message: fxcorepy.O2GMessageRow) -> bool:
        feature = message.feature
        if feature == self.__market_condition:
            text = message.text
            if self.__order.order_id in text:
                self.__reject_message = message.text
                return True
        return False
#------------------------#
 # BatchOrderMonitor.py
 
class BatchOrderMonitor:
    __request_ids = None
    __monitors = []

    def __init__(self) -> None:
        pass

    @property
    def monitors(self) -> List[OrderMonitor]:
        return self.__monitors

    @property
    def is_batch_executed(self) -> bool:
        all_completed = True
        for monitor in self.__monitors:
            if monitor.is_order_completed:
                self.remove_request_id(monitor.order.request_id)
            else:
                all_completed = False
        return len(self.__request_ids) == 0 and all_completed

    def set_request_ids(self, request_ids: List[str]) -> None:
        self.__request_ids = request_ids

    def on_request_completed(self, request_id: str, response: fxcorepy.O2GResponse) -> None:
        pass
    
    def remove_request_id(self, request_id: str) -> None:
        if self.is_own_request(request_id):
            self.__request_ids.remove(request_id)

    def on_request_failed(self, request_id: str) -> None:
        self.remove_request_id(request_id)

    def on_trade_added(self, trade_row: fxcorepy.O2GTradeRow) -> None:
        for monitor in self.__monitors:
            monitor.on_trade_added(trade_row)

    def on_order_added(self, order: fxcorepy.O2GOrderRow) -> None:
        request_id = order.request_id
        print("Order Added " + order.order_id)
        if self.is_own_request(request_id):
            if OrderMonitor.is_closing_order(order) or OrderMonitor.is_opening_order(order):
                self._add_to_monitoring(order)

    def on_order_deleted(self, order: fxcorepy.O2GOrderRow) -> None:
        for monitor in self.__monitors:
            monitor.on_order_deleted(order)

    def on_message_added(self, message: fxcorepy.O2GMessageRow) -> None:
        for monitor in self.__monitors:
            monitor.on_message_added(message)

    def on_closed_trade_added(self, close_trade_row: fxcorepy.O2GClosedTradeRow) -> None:
        for monitor in self.__monitors:
            monitor.on_closed_trade_added(close_trade_row)

    def is_own_request(self, request_id: str) -> bool:
        return request_id in self.__request_ids

    def _add_to_monitoring(self, order: fxcorepy.O2GOrderRow) -> None:
        self.__monitors.append(OrderMonitor(order))
#------------------------#

# OrderMonitorNetting.py


class OrderMonitorNetting:

    class ExecutionResult(Enum):
        EXECUTING = 1
        EXECUTED = 2
        PARTIAL_REJECTED = 3
        FULLY_REJECTED = 4
        CANCELED = 5

    class OrderState(Enum):
        ORDER_EXECUTING = 1
        ORDER_EXECUTED = 2
        ORDER_CANCELED = 3
        ORDER_REJECTED = 4
    
    __market_condition = "5"

    def __init__(self, order: fxcorepy.O2GOrderRow, i_net_position_amount: int = 0) -> None:
        self.__order = order
        self.__trades = []
        self.__updated_trades = []
        self.__closed_trades = []
        self.__state = OrderMonitorNetting.OrderState.ORDER_EXECUTING
        self.__result = OrderMonitorNetting.ExecutionResult.EXECUTING
        self.__total_amount = 0
        self.__reject_amount = 0
        self.__reject_message = ""
        self.__initial_amount = i_net_position_amount

    @staticmethod
    def is_opening_order(order: fxcorepy.O2GOrderRow) -> bool:
        return order.type.startswith("O")

    @staticmethod
    def is_closing_order(order: fxcorepy.O2GOrderRow) -> bool:
        return order.type.startswith("C")

    # Process trade adding during order execution
    def on_trade_added(self, trade: fxcorepy.O2GTradeRow) -> None:
        trade_order_id = trade.open_order_id
        order_id = self.__order.order_id
        if trade_order_id == order_id:
            self.__trades.append(trade)
            if self.__state == OrderMonitorNetting.OrderState.ORDER_EXECUTED or \
                    self.__state == OrderMonitorNetting.OrderState.ORDER_REJECTED or \
                    self.__state == OrderMonitorNetting.OrderState.ORDER_CANCELED:
                if self.is_all_trades_received:
                    self.set_result(True)

    # Process trade updating during order execution
    def on_trade_updated(self, trade_row: fxcorepy.O2GTradeRow) -> None:
        s_trade_order_id = trade_row.open_order_id
        s_order_id = self.__order.order_id
        if s_trade_order_id == s_order_id:
            self.__updated_trades.append(trade_row)
            if self.__state == OrderMonitorNetting.OrderState.ORDER_EXECUTED or \
                    self.__state == OrderMonitorNetting.OrderState.ORDER_REJECTED or \
                    self.__state == OrderMonitorNetting.OrderState.ORDER_CANCELED:
                if self.is_all_trades_received:
                    self.set_result(True)

    # Process trade closing during order execution
    def on_closed_trade_added(self, closed_trade: fxcorepy.O2GClosedTradeRow) -> None:
        order_id = self.__order.order_id
        closed_trade_order_id = closed_trade.close_order_id
        if order_id == closed_trade_order_id:
            self.__closed_trades.append(closed_trade)
            if self.__state == OrderMonitorNetting.OrderState.ORDER_EXECUTED or \
                    self.__state == OrderMonitorNetting.OrderState.ORDER_REJECTED or \
                    self.__state == OrderMonitorNetting.OrderState.ORDER_CANCELED:
                if self.is_all_trades_received:
                    self.set_result(True)

    # Process order deletion as result of execution
    def on_order_deleted(self, order: fxcorepy.O2GOrderRow) -> None:
        deleted_order_id = order.order_id
        order_id = self.__order.order_id
        if deleted_order_id == order_id:
            # Store Reject amount
            if order.Status.startswith("R"):
                self.__state = OrderMonitorNetting.OrderState.ORDER_REJECTED
                self.__reject_amount = order.amount
                self.__total_amount = order.origin_amount - self.__reject_amount
                if self.__reject_message != "" and self.is_all_trades_received:
                    self.set_result(True)
            else:
                if order.Status.startswith("C"):
                    self.__state = OrderMonitorNetting.OrderState.ORDER_CANCELED
                    self.__reject_amount = order.amount
                    self.__total_amount = order.origin_amount - self.__reject_amount
                    if self.is_all_trades_received:
                        self.set_result(False)
                else:
                    self.__reject_amount = 0
                    self.__total_amount = order.OriginAmount
                    self.__state = OrderMonitorNetting.OrderState.ORDER_EXECUTED
                    if self.is_all_trades_received:
                        self.set_result(True)

    def on_message_added(self, message: fxcorepy.O2GMessageRow) -> None:
        if self.__state == OrderMonitorNetting.OrderState.ORDER_REJECTED or \
                self.__state == OrderMonitorNetting.OrderState.ORDER_EXECUTING:
            is_reject_message = self.check_and_store_message(message)
            if self.__state == OrderMonitorNetting.OrderState.ORDER_REJECTED and is_reject_message:
                self.set_result(True)

    @property
    def order_row(self) -> fxcorepy.O2GOrderRow:
        return self.__order

    @property
    def trade_rows(self) -> List[fxcorepy.O2GTradeRow]:
        return self.__trades

    @property
    def updated_trade_rows(self) -> List[fxcorepy.O2GTradeRow]:
        return self.__updated_trades

    @property
    def closed_trade_rows(self) -> List[fxcorepy.O2GClosedTradeRow]:
        return self.__closed_trades

    @property
    def reject_amount(self) -> int:
        return self.__reject_amount

    @property
    def reject_message(self) -> str:
        return self.__reject_message

    @property
    def result(self) -> ExecutionResult:
        return self.__result

    @property
    def is_order_completed(self) -> bool:
        return self.__result != OrderMonitorNetting.ExecutionResult.EXECUTING

    def check_and_store_message(self, message: fxcorepy.O2GMessageRow) -> bool:
        feature = message.feature
        if feature == self.__market_condition:
            text = message.text
            if self.__order.order_id in text:
                self.__reject_message = message.text
                return True
        return False

    @property
    def is_all_trades_received(self) -> bool:
        if self.__state == OrderMonitorNetting.OrderState.ORDER_EXECUTING:
            return False
        i_current_total_amount = 0
        for trade in self.__trades:
            i_current_total_amount += trade.amount

        for trade in self.__updated_trades:
            i_current_total_amount += trade.amount
        
        for trade in self.__closed_trades:
            i_current_total_amount += trade.amount

        return abs(i_current_total_amount - self.__initial_amount) == self.__total_amount

    def set_result(self, success: bool) -> None:
        if success:
            if self.__reject_amount == 0:
                self.__result = OrderMonitorNetting.ExecutionResult.EXECUTED
            else:
                self.__result = OrderMonitorNetting.ExecutionResult.FULLY_REJECTED \
                    if (len(self.__trades) == 0 and len(self.__closed_trades) == 0) \
                    else OrderMonitorNetting.ExecutionResult.PARTIAL_REJECTED
            
        else:
            self.__result = OrderMonitorNetting.ExecutionResult.CANCELED
#------------------------#

# TableListenerContainer.py



import traceback

try:
    # Try to import ForexConnect and Common from forexconnect
    from forexconnect import ForexConnect, Common
except ModuleNotFoundError:
    # If that fails, try to import ForexConnect and Common directly
    try:
        from .forexconnect.ForexConnect import ForexConnect, Common
    except ModuleNotFoundError:
        # If that also fails, print an error message
        print("Could not import ForexConnect or Common. Please ensure the modules are installed and available.")





class TableListenerContainer:
    __response_listener = None
    __request_id = ""
    __order_monitor = None

    def __init__(self, response_listener, fx):
        self.__response_listener = response_listener
        self._fx = fx
        self._listeners = []

    def set_request_id(self, request_id):
        self.__request_id = request_id

    def _on_added_orders(self, listener, row_id, order_row):
        del listener, row_id
        if self.__request_id == order_row.request_id:
            if OrderMonitor.is_closing_order(
                    order_row) or OrderMonitor.is_opening_order(
                        order_row) and self.__order_monitor is None:
                print(
                    "The order has been added. Order ID: {0:s}, Rate: {1:.5f}, Time In Force: {2:s}".format(
                        order_row.order_id, order_row.rate,
                        order_row.time_in_force))
                self.__order_monitor = OrderMonitor(order_row)

    def _on_added_trades(self, listener, row_id, trade_row):
        del listener, row_id
        if self.__order_monitor is not None:
            self.__order_monitor.on_trade_added(trade_row)
            if self.__order_monitor.is_order_completed:
                self._print_result()
                self.__response_listener.stop_waiting()

    def _on_added_closed_trades(self, listener, row_id, closed_trade_row):
        del listener, row_id
        if self.__order_monitor is not None:
            self.__order_monitor.on_closed_trade_added(closed_trade_row)
            if self.__order_monitor.is_order_completed:
                self._print_result()
                self.__response_listener.stop_waiting()

    def _on_added_messages(self, listener, row_id, message_row):
        del listener, row_id
        if self.__order_monitor is not None:
            self.__order_monitor.on_message_added(message_row)
            if self.__order_monitor.is_order_completed:
                self._print_result()
                self.__response_listener.stop_waiting()

    def _on_deleted_orders(self, listener, row_id, row_data):
        del listener, row_id
        order_row = row_data
        if self.__request_id == order_row.request_id:
            if self.__order_monitor is not None:
                print("The order has been deleted. Order ID: {0}".format(
                    order_row.order_id))
                self.__order_monitor.on_order_deleted(order_row)
                if self.__order_monitor.is_order_completed:
                    self._print_result()
                    self.__response_listener.stop_waiting()

    def _print_result_canceled(self, order_id, trades, closed_trades):
        if len(trades) > 0:
            self._print_trades(trades, order_id)
            self._print_closed_trades(closed_trades, order_id)
            print("A part of the order has been canceled. Amount = {0}".format(
                self.__order_monitor.reject_amount))
        else:
            print("The order: OrderID = {0}  has been canceled".format(
                order_id))
            print("The cancel amount = {0}".format(
                self.__order_monitor.reject_amount))

    def _print_result_fully_rejected(self, order_id, trades, closed_trades):
        del trades, closed_trades
        print("The order has been rejected. OrderID = {0}".format(
            order_id))
        print("The rejected amount = {0}".format(
            self.__order_monitor.reject_amount))
        print("Rejection cause: {0}".format(
            self.__order_monitor.reject_message))

    def _print_result_partial_rejected(self, order_id, trades, closed_trades):
        self._print_trades(trades, order_id)
        self._print_closed_trades(closed_trades, order_id)
        print("A part of the order has been rejected. Amount = {0}".format(
            self.__order_monitor.reject_amount))
        print("Rejection cause: {0} ".format(
            self.__order_monitor.reject_message))

    def _print_result_executed(self, order_id, trades, closed_trades):
        self._print_trades(trades, order_id)
        self._print_closed_trades(closed_trades, order_id)

    def _print_result(self):
        if self.__order_monitor is not None:
            result = self.__order_monitor.result
            order = self.__order_monitor.order_row
            order_id = order.order_id
            trades = self.__order_monitor.trade_rows
            closed_trades = self.__order_monitor.closed_trade_rows

            print_result_func = {
                OrderMonitor.ExecutionResult.CANCELED: self._print_result_canceled,
                OrderMonitor.ExecutionResult.FULLY_REJECTED: self._print_result_fully_rejected,
                OrderMonitor.ExecutionResult.PARTIAL_REJECTED: self._print_result_partial_rejected,
                OrderMonitor.ExecutionResult.EXECUTED: self._print_result_executed
            }
            try:
                print_result_func[result](order_id, trades, closed_trades)
            except KeyError:
                pass
            except Exception as e:
                print("Exception: {0}\n".format(e))
                print(traceback.format_exc())

    @staticmethod
    def _print_trades(trades, order_id):
        if len(trades) == 0:
            return
        print(
            "For the order: OrderID = {0} the following positions have been opened:".format(
                order_id))

        for trade in trades:
            trade_id = trade.trade_id
            amount = trade.amount
            rate = trade.open_rate
            print(
                "Trade ID: {0:s}; Amount: {1:d}; Rate: {2:.5f}".format(trade_id,
                                                                       amount,
                                                                       rate))

    @staticmethod
    def _print_closed_trades(closed_trades, order_id):
        if len(closed_trades) == 0:
            return
        print(
            "For the order: OrderID = {0} the following positions have been closed: ".format(
                order_id))

        for closed_trade in closed_trades:
            trade_id = closed_trade.trade_id
            amount = closed_trade.amount
            rate = closed_trade.close_rate
            print(
                "Closed Trade ID: {0:s}; Amount: {1:d}; Closed Rate: {2:.5f}".format(
                    trade_id, amount, rate))

    def subscribe_events(self):
        orders_table = self._fx.get_table(ForexConnect.ORDERS)
        orders_table_listener = Common.subscribe_table_updates(orders_table,
                                                               on_add_callback=self._on_added_orders,
                                                               on_delete_callback=self._on_deleted_orders)
        self._listeners.append(orders_table_listener)

        trades_table = self._fx.get_table(ForexConnect.TRADES)
        trades_table_listener = Common.subscribe_table_updates(trades_table,
                                                               on_add_callback=self._on_added_trades)
        self._listeners.append(trades_table_listener)

        messages_table = self._fx.get_table(ForexConnect.MESSAGES)
        messages_table_listener = Common.subscribe_table_updates(messages_table,
                                                                 on_add_callback=self._on_added_messages)
        self._listeners.append(messages_table_listener)

        closed_trades_table = self._fx.get_table(ForexConnect.CLOSED_TRADES)
        closed_trades_table_listener = Common.subscribe_table_updates(closed_trades_table,
                                                                      on_add_callback=self._on_added_closed_trades)
        self._listeners.append(closed_trades_table_listener)

    def unsubscribe_events(self):
        for listener in self._listeners:
            listener.unsubscribe()
        self._listeners = []
#------------------------#

# common.py


import logging
import datetime
import traceback
import argparse
import sys


try :
    import __main__
    logging.basicConfig(filename='{0}.log'.format(__main__.__file__), level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s', datefmt='%m.%d.%Y %H:%M:%S')
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)
except:
    print('logging failed - dont worry')

def add_main_arguments(parser: argparse.ArgumentParser):
    parser.add_argument('--login',
                        metavar="LOGIN",
                        required=True,
                        help='Your user name.')

    parser.add_argument('--password',
                        metavar="PASSWORD",
                        required=True,
                        help='Your password.')

    parser.add_argument('--urlserver',
                        metavar="URL",
                        required=True,
                        help='The server URL. For example,\
                                 https://www.fxcorporate.com/Hosts.jsp.')

    parser.add_argument('--connection',
                        metavar="CONNECTION",
                        required=True,
                        help='The connection name. For example, \
                                 "Demo" or "Real".')


    parser.add_argument('-session',
                        help='The database name. Required only for users who\
                                 have accounts in more than one database.\
                                 Optional parameter.')

    parser.add_argument('-pin',
                        help='Your pin code. Required only for users who have \
                                 a pin. Optional parameter.')

def add_candle_open_price_mode_argument(parser: argparse.ArgumentParser):
    parser.add_argument('--openpricemode',
                        metavar="CANDLE_OPEN_PRICE_MODE",
                        default="prev_close",
                        help='Ability to set the open price candles mode. \
                        Possible values are first_tick, prev_close. For more information see description \
                        of O2GCandleOpenPriceMode enumeration. Optional parameter.')

def add_instrument_timeframe_arguments(parser: argparse.ArgumentParser, timeframe: bool = True):
    parser.add_argument('-i','--instrument',
                        metavar="INSTRUMENT",
                        default="EUR/USD",
                        help='An instrument which you want to use in sample. \
                                  For example, "EUR/USD".')

    if timeframe:
        parser.add_argument('-t','--timeframe',
                            metavar="TIMEFRAME",
                            default="m5",
                            help='Time period which forms a single candle. \
                                      For example, m1 - for 1 minute, H1 - for 1 hour.')
    parser.add_argument('-ip',
                        metavar="IndicatorPattern",
                        required=False,
                        help='The indicator Pattern. For example, \
                                 "AOAC","JTL,"JTLAOAC","JTLAOAC","AOACMFI".')

def add_direction_rate_lots_arguments(parser: argparse.ArgumentParser, direction: bool = True, rate: bool = True,
                                      lots: bool = True):
    if direction:
        parser.add_argument('-d', metavar="TYPE", required=True,
                            help='The order direction. Possible values are: B - buy, S - sell.')
    if rate:
        parser.add_argument('-r', metavar="RATE", required=True, type=float,
                            help='Desired price of an entry order.')
    if lots:
        parser.add_argument('-lots', metavar="LOTS", default=1, type=int,
                            help='Trade amount in lots.')


def add_account_arguments(parser: argparse.ArgumentParser):
    parser.add_argument('-account', metavar="ACCOUNT",
                        help='An account which you want to use in sample.')


def valid_datetime(check_future: bool):
    def _valid_datetime(str_datetime: str):
        date_format = '%m.%d.%Y %H:%M:%S'
        try:
            result = datetime.datetime.strptime(str_datetime, date_format).replace(
                tzinfo=datetime.timezone.utc)
            if check_future and result > datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc):
                msg = "'{0}' is in the future".format(str_datetime)
                raise argparse.ArgumentTypeError(msg)
            return result
        except ValueError:
            now = datetime.datetime.now()
            msg = "The date '{0}' is invalid. The valid data format is '{1}'. Example: '{2}'".format(
                str_datetime, date_format, now.strftime(date_format))
            raise argparse.ArgumentTypeError(msg)
    return _valid_datetime


def add_date_arguments(parser: argparse.ArgumentParser, date_from: bool = True, date_to: bool = True):
    if date_from:
        parser.add_argument('-s','--datefrom',
                            metavar="\"m.d.Y H:M:S\"",
                            help='Date/time from which you want to receive\
                                      historical prices. If you leave this argument as it \
                                      is, it will mean from last trading day. Format is \
                                      "m.d.Y H:M:S". Optional parameter.',
                            type=valid_datetime(True)
                            )
    if date_to:
        parser.add_argument('-e','--dateto',
                            metavar="\"m.d.Y H:M:S\"",
                            help='Datetime until which you want to receive \
                                      historical prices. If you leave this argument as it is, \
                                      it will mean to now. Format is "m.d.Y H:M:S". \
                                      Optional parameter.',
                            type=valid_datetime(False)
                            )


def add_report_date_arguments(parser: argparse.ArgumentParser, date_from: bool = True, date_to: bool = True):
    if date_from:
        parser.add_argument('-s','--datefrom',
                            metavar="\"m.d.Y H:M:S\"",
                            help='Datetime from which you want to receive\
                                      combo account statement report. If you leave this argument as it \
                                      is, it will mean from last month. Format is \
                                      "m.d.Y H:M:S". Optional parameter.',
                            type=valid_datetime(True)
                            )
    if date_to:
        parser.add_argument('-e','--dateto',
                            metavar="\"m.d.Y H:M:S\"",
                            help='Datetime until which you want to receive \
                                      combo account statement report. If you leave this argument as it is, \
                                      it will mean to now. Format is "m.d.Y H:M:S". \
                                      Optional parameter.',
                            type=valid_datetime(True)
                            )


def add_max_bars_arguments(parser: argparse.ArgumentParser):
    parser.add_argument('-c','--quotescount',
                        metavar="MAX",
                        default=335,
                        type=int,
                        help='Max number of bars. 0 - Not limited')


# def add_bars_arguments(parser: argparse.ArgumentParser):
#     parser.add_argument('-bars',
#                         metavar="COUNT",
#                         default=3,
#                         type=int,
#                         help='Build COUNT bars. Optional parameter.')


def add_output_argument(parser: argparse.ArgumentParser):
    """
    Adds an output argument to the given argument parser.

    Args:
        parser (argparse.ArgumentParser): The argument parser to add the output argument to.

    Returns:
        None
    """
    parser.add_argument('-o','--output',
                        action='store_true',
                        help='Output file. If specified, output will be written in the filestore.')
    
    parser.add_argument('-z','--compress',
                        action='store_true',
                        help='Compress the output. If specified, it will also activate the output flag.')

    return parser


# def add_quiet_argument(parser):
#     parser.add_argument('-q','--quiet',
#                         action='store_true',
#                         help='Suppress all output. If specified, no output will be printed to the console.')
#     return parser

def add_verbose_argument(parser):
    parser.add_argument('-v', '--verbose',
                        type=int,
                        default=0,
                        help='Set the verbosity level. 0 = quiet, 1 = normal, 2 = verbose, 3 = very verbose, etc.')
    return parser

def add_cds_argument(parser):
    parser.add_argument('-cds','--cds',
                        action='store_true',
                        help='Action the creation of CDS')
    return parser


def print_exception(exception: Exception):
    logging.error("Exception: {0}\n{1}".format(exception, traceback.format_exc()))



connection_status="DISCONNECTED"
def get_connection_status():
    global connection_status
    return connection_status

quiet=False
# function for print available descriptors
def session_status_changed(session: fxcorepy.O2GSession,
                           status: fxcorepy.AO2GSessionStatus.O2GSessionStatus):
    global connection_status
    connection_status= status
    if not quiet:
        logging.info("Status: " + str(status))
    if status == fxcorepy.AO2GSessionStatus.O2GSessionStatus.TRADING_SESSION_REQUESTED:
        descriptors = session.trading_session_descriptors
        logging.info("Session descriptors:")
        logging.info(" {0:>7} | {1:>7} | {2:>30} | {3:>7}\n".format("id", "name", "description", "requires pin"))
        for desc in descriptors:
            logging.info(" {0:>7} | {1:>7} | {2:>30} | {3:>7}\n".format(desc.id, desc.name,
                                                                        desc.description,
                                                                        str(desc.requires_pin)))











def diff_month(year: int, month: int, date2: datetime):
    return (year - date2.year) * 12 + month - date2.month






#@STCIssue in less todo
def convert_timeframe_to_seconds(unit: fxcorepy.O2GTimeFrameUnit, size: int):
    current_unit = unit
    current_size = size
    step = 1
    if current_unit == fxcorepy.O2GTimeFrameUnit.MIN:
        step = 60  # leads to seconds
    elif current_unit == fxcorepy.O2GTimeFrameUnit.HOUR:
        step = 60*60
    elif current_unit == fxcorepy.O2GTimeFrameUnit.DAY:
        step = 60*60*24
    elif current_unit == fxcorepy.O2GTimeFrameUnit.WEEK:
        step = 60*60*24*7
    elif current_unit == fxcorepy.O2GTimeFrameUnit.MONTH:
        step = 60 * 60 * 24 * 30
    elif current_unit == fxcorepy.O2GTimeFrameUnit.TICK:
        step = 1
    return step * current_size
#------------------------#


_JGT_CONFIG_JSON_SECRET=None

def readconfig(json_config_str=None):
    global _JGT_CONFIG_JSON_SECRET
    # Try reading config file from current directory

    if json_config_str is not None:
        config = json.loads(json_config_str)
        _JGT_CONFIG_JSON_SECRET=json_config_str
        return config


    if _JGT_CONFIG_JSON_SECRET is not None:
        config = json.loads(_JGT_CONFIG_JSON_SECRET)
        return config
    
    # Otherwise, try reading config file from current directory, home or env var
    config_file = 'config.json'
    config = None

    if os.path.isfile(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
            return config
    else:
        # If config file not found, check home directory
        home_dir = os.path.expanduser("~")
        config_file = os.path.join(home_dir, 'config.json')
        if os.path.isfile(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
        else:
            # If config file still not found, try reading from environment variable
            config_json_str = os.getenv('JGT_CONFIG_JSON_SECRET')
            if config_json_str:
                config = json.loads(config_json_str)
                return config


    # Now you can use the config dictionary in your application

    # Read config file
    with open(config_file, 'r') as file:
        config = json.load(file)
        
    if config is None:
        raise Exception("Configuration not found")
    
    return config
