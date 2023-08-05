# Factura.com Python Wrapper

This is a simple wrapper for the `factura.com` REST API, it includes some helper
functions that enable the usage of specified endpoints

## Installation

Module can be installed using pip package library

```bash
$ pip install facturacom
```

## Modules

At this time the only modules supported by this wrapper are:
- Clients
- CFDI

## Usage

Some examples on how to use the api wrapper

### Clients

#### List all

```python
import facturacom
from facturacom.clients import Clients

facturacom.DEBUG = True # Environment to send requests
facturacom.FACTURACOM_API_KEY = API_KEY
facturacom.FACTURACOM_SECRET_KEY = SECRET_KEY

clients = Clients.list_all() # Shows all clients on account
```

#### Create

```python
import facturacom
from facturacom.clients import Clients

facturacom.DEBUG = True # Environment to send requests
facturacom.FACTURACOM_API_KEY = API_KEY
facturacom.FACTURACOM_SECRET_KEY = SECRET_KEY
clients = Clients.create({
    'nombre': 'Nombre',
    'apellidos': 'Apellidos',
    'email': 'example@gmail.com',
    'telefono': '4433223322',
    'razons': 'Razon Social del RFC',
    'rfc': 'TATR72052169A',
    'calle': 'Av. Castorena',
    'numero_exterior': '30',
    'numero_interior': '32',
    'codpos': '05000',
    'colonia': 'Cuajimalpa',
    'estado': 'Ciudad de Mexico',
    'ciudad': 'Ciudad de Mexico',
    'delegacion': 'Cuajimalpa'
})
```

#### Update

```python
import facturacom
from facturacom.clients import Clients

facturacom.DEBUG = True # Environment to send requests
facturacom.FACTURACOM_API_KEY = API_KEY
facturacom.FACTURACOM_SECRET_KEY = SECRET_KEY

clients = Clients.update('Unique facturacom ID', {
    'nombre': 'Nombre',
    'apellidos': 'Apellidos',
    'email': 'example@gmail.com',
    'telefono': '4433223322',
    'razons': 'Razon Social del RFC',
    'rfc': 'TATR72052169A',
    'calle': 'Av. Castorena',
    'numero_exterior': '30',
    'numero_interior': '32',
    'codpos': '05000',
    'colonia': 'Cuajimalpa',
    'estado': 'Ciudad de Mexico',
    'ciudad': 'Ciudad de Mexico',
    'delegacion': 'Cuajimalpa'
})
```

#### Find

```python
import facturacom
from facturacom.clients import Clients

facturacom.DEBUG = True # Environment to send requests
facturacom.FACTURACOM_API_KEY = API_KEY
facturacom.FACTURACOM_SECRET_KEY = SECRET_KEY

clients = Clients.find(RFC) # Finds client by RFC on account
```

### CFDI

#### List all

```python
import facturacom
from facturacom.cfdi import Cfdi

facturacom.DEBUG = True # Environment to send requests
facturacom.FACTURACOM_API_KEY = API_KEY
facturacom.FACTURACOM_SECRET_KEY = SECRET_KEY
cfdis = Cfdi.list_all()
```

#### Create

```python
import facturacom
from facturacom.cfdi import Cfdi

facturacom.DEBUG = True # Environment to send requests
facturacom.FACTURACOM_API_KEY = API_KEY
facturacom.FACTURACOM_SECRET_KEY = SECRET_KEY
cfdis = Cfdi.create({
  "Receptor": {
      "UID": "5a9c6ccb26e36",
      "ResidenciaFiscal": "023203d",
  },
  "TipoDocumento":"factura",
  "Conceptos": [{
      "ClaveProdServ": "25181608",
      "NoIdentificacion": "SKU-12122",
      "Cantidad": 10,
      "ClaveUnidad": "E48",
      "Unidad": "Unidad de servicio",
      "ValorUnitario": 1500,
      "Descripcion": 'Diseno de interfaces para sitio web',
      "Descuento": 0,
      "Impuestos": {
          "Traslados": [{
              "Base" : 15000,
              "Impuesto": "002",
              "TipoFactor": "Tasa",
              "TasaOCuota": 0.16,
              "Importe": 2400
          }],
          "Retenidos": [{
              "Base" : 15000,
              "Impuesto": "001",
              "TipoFactor": "Tasa",
              "TasaOCuota": 0.10,
              "Importe": 1500
          }],
          "Locales": [{
              "Impuesto": "ISH",
              "TasaOCuota": 0.03
          }]
      },
  }],
  "UsoCFDI": "G02",
  "Serie":"1215",
  "FormaPago":"03",
  "MetodoPago": "PUE",
  "CondicionesDePago": "Pago en 10 dias",
  "Moneda": "MXN",
  "TipoCambio": 19.89,
  "NumOrder": "MY-Order-10",
  "FechaFromAPI": datetime.now().replace(microsecond=0).isoformat(),
  "Comentarios": "Comentarios para agregar a la factura PDF",
  "EnviarCorreo": False
})
```

#### Cancel

```python
import facturacom
from facturacom.cfdi import Cfdi

facturacom.DEBUG = True # Environment to send requests
facturacom.FACTURACOM_API_KEY = API_KEY
facturacom.FACTURACOM_SECRET_KEY = SECRET_KEY
cfdi = Cfdi.cancel('Unique factura ID')
```

#### XML

```python
import facturacom
from facturacom.cfdi import Cfdi

facturacom.DEBUG = True # Environment to send requests
facturacom.FACTURACOM_API_KEY = API_KEY
facturacom.FACTURACOM_SECRET_KEY = SECRET_KEY
cfdi = Cfdi.xml('Unique facturacom ID') # This method returns a file object
```

#### PDF

```python
import facturacom
from facturacom.cfdi import Cfdi

facturacom.DEBUG = True # Environment to send requests
facturacom.FACTURACOM_API_KEY = API_KEY
facturacom.FACTURACOM_SECRET_KEY = SECRET_KEY
cfdis = Cfdi.pdf('unique facturacom ID') # This method returns a file object
```
