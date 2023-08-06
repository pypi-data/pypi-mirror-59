# TraceLogging for Python
This small package implements a `TraceLoggingProvider` for publishing ETW events in **Windows**.



**Use at your own risk.**

## Requirements
- python 3.8.x

## Installation
```bash
pip install tracelogging
```

## Usage
All usage examples are assuming an enabled EventTrace session for the provider(you can use [EtwConsumer](./SampleEtwConsumer/))):

### Basic logging for the extremely lazy
Similar usage to python's own logging. No handlers, no formatters, no `exception` method, no format or additional arguments supported.


The name given to a provider will be used to generate the appropriate GUID the same way `TraceEvent` does.
```py
import tracelogging
log = tracelogging.getLogger('MyLoggerName')

log.debug('ging')
log.info('rmation')
log.warning('be careful')
log.error('err')
log.critical('oh no!')
```


### Defining your very own provider
Defines a provider named `PythonProvider` that can publish an event named `BasicEvent` without any additional data
```py
from tracelogging import Provider, event

class PythonProvider(Provider):
    @event() # mind the parentheses
    def BasicEvent(self):
        pass

log = PythonProvider()
log.BasicEvent()
```




### Advanced usage
You can override the provider's `Name` directly by setting the `Name` class member to whatever you wish.
Same can be done with the `Guid` member, by setting it to an instance of `UUID` with the desired value.


You can set values for the event's descriptor using the `event` decoraotr, just like you would with `TraceEvent` ([or EVENT_DESCRIPTOR struct](https://docs.microsoft.com/en-us/windows/win32/api/evntprov/ns-evntprov-event_descriptor)). You may also specify an override to the event name.

In order to add data to the event, you must use python's type-hinting with the supported types(see Types)
```py
from tracelogging import Provider, event, Types, TraceLevel

class PythonProvider(Provider):
    Name = 'Company-Product-Component'

    @event(Name='FileSize', Id=1, Level=TraceLevel.Warning, Keyword=0x01)
    def not_a_nice_event_name(self, file_path:Types.UnicodeString, file_size:Types.UInt32):
        print('this will be called after the event is written, if you wish to implement anything here')

log = PythonProvider()
log.not_a_nice_event_name('C:\\windows\\system32\\calc.exe', 0x1000) # will send event named 'FileSize'
```

### Currently supported types
Type | Python
--|--
`UnicodeString` | `str`
`UInt32` | `int`

## Notes
- Read contents of `TraceLoggingProvider.h` header for more info
- Most logic is performed during provider class definition. Instanciation only registers and 'sets' the provider as one capable of sending self-described events
- Providers can inherit events from base classes, though doing so is discouraged.
- Internal code uses a sort of singleton to prevent multiple instances of the same provider

## License
MIT

## Troubleshooting
set environment variable `TLG_LOG` to the desired log level (1 for high verbosity, 0 to turn off)
