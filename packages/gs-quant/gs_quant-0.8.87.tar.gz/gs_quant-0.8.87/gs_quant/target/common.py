"""
Copyright 2019 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""

import datetime
from typing import Tuple, Union
from enum import Enum
from gs_quant.base import Base, EnumBase, InstrumentBase, Priceable, Scenario, camel_case_translate, get_enum_value


class AssetClass(EnumBase, Enum):    
    
    """Asset classification of security. Assets are classified into broad groups which
       exhibit similar characteristics and behave in a consistent way under
       different market conditions"""

    Cash = 'Cash'
    Commod = 'Commod'
    Credit = 'Credit'
    Cross_Asset = 'Cross Asset'
    Econ = 'Econ'
    Equity = 'Equity'
    Fund = 'Fund'
    FX = 'FX'
    Mortgage = 'Mortgage'
    Rates = 'Rates'
    Loan = 'Loan'
    
    def __repr__(self):
        return self.value


class AssetType(EnumBase, Enum):    
    
    """Asset type differentiates the product categorization or contract type"""

    Access = 'Access'
    Basis = 'Basis'
    BasisSwap = 'BasisSwap'
    Benchmark = 'Benchmark'
    Benchmark_Rate = 'Benchmark Rate'
    Bond = 'Bond'
    Calendar_Spread = 'Calendar Spread'
    Cap = 'Cap'
    Cash = 'Cash'
    Certificate = 'Certificate'
    CD = 'CD'
    Cliquet = 'Cliquet'
    Commodity = 'Commodity'
    CommodVarianceSwap = 'CommodVarianceSwap'
    Company = 'Company'
    Convertible = 'Convertible'
    Credit_Basket = 'Credit Basket'
    Cross = 'Cross'
    Crypto_Currency = 'Crypto Currency'
    CSL = 'CSL'
    Currency = 'Currency'
    Custom_Basket = 'Custom Basket'
    Default_Swap = 'Default Swap'
    Economic = 'Economic'
    Endowment = 'Endowment'
    Equity_Basket = 'Equity Basket'
    ETF = 'ETF'
    ETN = 'ETN'
    Event = 'Event'
    Fixing = 'Fixing'
    Floor = 'Floor'
    Forward = 'Forward'
    Future = 'Future'
    Hedge_Fund = 'Hedge Fund'
    Index = 'Index'
    InflationSwap = 'InflationSwap'
    Inter_Commodity_Spread = 'Inter-Commodity Spread'
    Market_Location = 'Market Location'
    Multi_Asset_Allocation = 'Multi-Asset Allocation'
    Mutual_Fund = 'Mutual Fund'
    Note = 'Note'
    Option = 'Option'
    Pension_Fund = 'Pension Fund'
    Preferred_Stock = 'Preferred Stock'
    Physical = 'Physical'
    Precious_Metal = 'Precious Metal'
    Reference_Entity = 'Reference Entity'
    Research_Basket = 'Research Basket'
    Rate = 'Rate'
    Risk_Premia = 'Risk Premia'
    Securities_Lending_Loan = 'Securities Lending Loan'
    Share_Class = 'Share Class'
    Single_Stock = 'Single Stock'
    Swap = 'Swap'
    Swaption = 'Swaption'
    Systematic_Hedging = 'Systematic Hedging'
    VarianceSwap = 'VarianceSwap'
    
    def __repr__(self):
        return self.value


class BusinessDayConvention(EnumBase, Enum):    
    
    """Business Day Convention"""

    Following = 'Following'
    Modified_Following = 'Modified Following'
    Previous = 'Previous'
    Unadjusted = 'Unadjusted'
    
    def __repr__(self):
        return self.value


class BuySell(EnumBase, Enum):    
    
    """Buy or Sell side of contract"""

    Buy = 'Buy'
    Sell = 'Sell'
    
    def __repr__(self):
        return self.value


class ClaimType(EnumBase, Enum):    
    
    """Claim Type with reference to a position."""

    Receiver = 'Receiver'
    Payer = 'Payer'
    
    def __repr__(self):
        return self.value


class CommodityAsset(EnumBase, Enum):    
    
    """Commodity asset"""

    Aluminium = 'Aluminium'
    Aluminium_Alloy = 'Aluminium Alloy'
    Chicago_Ethanol = 'Chicago Ethanol'
    Coal = 'Coal'
    Coffee = 'Coffee'
    Copper = 'Copper'
    Corn = 'Corn'
    Cotton = 'Cotton'
    Crude_Palm_Oil = 'Crude Palm Oil'
    Diesel_Fuel = 'Diesel Fuel'
    Electricity = 'Electricity'
    Emissions = 'Emissions'
    Ethylene = 'Ethylene'
    Freight = 'Freight'
    Fuel_Oil = 'Fuel Oil'
    Gas_Oil = 'Gas Oil'
    Gasoline = 'Gasoline'
    Gold = 'Gold'
    Heating_Oil = 'Heating Oil'
    Iron_Ore = 'Iron Ore'
    Jet_Fuel = 'Jet Fuel'
    Lead = 'Lead'
    Lean_Hogs = 'Lean Hogs'
    NGL = 'NGL'
    Naphtha = 'Naphtha'
    Natural_Gas = 'Natural Gas'
    Nickel = 'Nickel'
    Oil = 'Oil'
    Palladium = 'Palladium'
    Platinum = 'Platinum'
    Polypropylene = 'Polypropylene'
    Primary_Aluminium = 'Primary Aluminium'
    Silver = 'Silver'
    Soybean_Meal = 'Soybean Meal'
    Soybean_Oil = 'Soybean Oil'
    Soybeans = 'Soybeans'
    Sugar = 'Sugar'
    Tin = 'Tin'
    Ultra_Low_Sulphur_Diesel = 'Ultra Low Sulphur Diesel'
    Wheat = 'Wheat'
    White_Sugar = 'White Sugar'
    Zinc = 'Zinc'
    
    def __repr__(self):
        return self.value


class CommodityMeanRule(EnumBase, Enum):    
    
    """Commodity mean rule"""

    Do_Not_Remove = 'Do Not Remove'
    Remove_Calculated = 'Remove Calculated'
    Remove_Fixed = 'Remove Fixed'
    
    def __repr__(self):
        return self.value


class CountryCode(EnumBase, Enum):    
    
    """ISO Country code"""

    AU = 'AU'
    CX = 'CX'
    CC = 'CC'
    HM = 'HM'
    NF = 'NF'
    NZ = 'NZ'
    CK = 'CK'
    NU = 'NU'
    TK = 'TK'
    JP = 'JP'
    JN = 'JN'
    EU = 'EU'
    ER = 'ER'
    EZ = 'EZ'
    AT = 'AT'
    BE = 'BE'
    FI = 'FI'
    FR = 'FR'
    GF = 'GF'
    PF = 'PF'
    TF = 'TF'
    GP = 'GP'
    MQ = 'MQ'
    YT = 'YT'
    NC = 'NC'
    RE = 'RE'
    SH = 'SH'
    PM = 'PM'
    WF = 'WF'
    DE = 'DE'
    GE = 'GE'
    GR = 'GR'
    IE = 'IE'
    IT = 'IT'
    LU = 'LU'
    NL = 'NL'
    AW = 'AW'
    AN = 'AN'
    PT = 'PT'
    ES = 'ES'
    BY = 'BY'
    CH = 'CH'
    SE = 'SE'
    SW = 'SW'
    DK = 'DK'
    FO = 'FO'
    NO = 'NO'
    BV = 'BV'
    SJ = 'SJ'
    LI = 'LI'
    GB = 'GB'
    UK = 'UK'
    AI = 'AI'
    IO = 'IO'
    KY = 'KY'
    FK = 'FK'
    GI = 'GI'
    MS = 'MS'
    PN = 'PN'
    GS = 'GS'
    TC = 'TC'
    VG = 'VG'
    JE = 'JE'
    _02 = '02'
    US = 'US'
    AS = 'AS'
    GU = 'GU'
    MP = 'MP'
    PR = 'PR'
    UM = 'UM'
    VI = 'VI'
    CA = 'CA'
    AR = 'AR'
    BA = 'BA'
    BD = 'BD'
    BG = 'BG'
    BS = 'BS'
    BM = 'BM'
    BO = 'BO'
    BR = 'BR'
    CL = 'CL'
    CN = 'CN'
    CO = 'CO'
    CR = 'CR'
    CZ = 'CZ'
    DO = 'DO'
    EC = 'EC'
    EG = 'EG'
    GA = 'GA'
    GT = 'GT'
    HK = 'HK'
    HR = 'HR'
    HU = 'HU'
    IL = 'IL'
    IM = 'IM'
    IR = 'IR'
    IS = 'IS'
    JO = 'JO'
    KE = 'KE'
    KR = 'KR'
    KZ = 'KZ'
    LB = 'LB'
    LK = 'LK'
    LT = 'LT'
    MA = 'MA'
    MH = 'MH'
    ML = 'ML'
    MO = 'MO'
    MT = 'MT'
    MX = 'MX'
    MY = 'MY'
    NI = 'NI'
    OM = 'OM'
    PA = 'PA'
    PD = 'PD'
    PE = 'PE'
    PH = 'PH'
    PK = 'PK'
    PL = 'PL'
    QA = 'QA'
    RO = 'RO'
    RU = 'RU'
    SA = 'SA'
    SG = 'SG'
    SI = 'SI'
    SK = 'SK'
    SV = 'SV'
    TH = 'TH'
    TN = 'TN'
    TP = 'TP'
    TR = 'TR'
    TW = 'TW'
    UA = 'UA'
    UY = 'UY'
    VE = 'VE'
    VN = 'VN'
    ZA = 'ZA'
    BH = 'BH'
    EE = 'EE'
    GH = 'GH'
    ME = 'ME'
    RS = 'RS'
    ZM = 'ZM'
    ZW = 'ZW'
    TT = 'TT'
    AE = 'AE'
    KW = 'KW'
    BB = 'BB'
    LV = 'LV'
    GG = 'GG'
    CY = 'CY'
    CI = 'CI'
    MU = 'MU'
    PY = 'PY'
    HN = 'HN'
    BZ = 'BZ'
    NA = 'NA'
    FJ = 'FJ'
    BW = 'BW'
    DZ = 'DZ'
    MN = 'MN'
    SN = 'SN'
    TZ = 'TZ'
    AD = 'AD'
    AG = 'AG'
    AL = 'AL'
    AM = 'AM'
    AO = 'AO'
    AZ = 'AZ'
    BF = 'BF'
    BI = 'BI'
    BJ = 'BJ'
    BN = 'BN'
    BT = 'BT'
    CD = 'CD'
    CF = 'CF'
    CG = 'CG'
    CM = 'CM'
    CU = 'CU'
    CV = 'CV'
    CS = 'CS'
    DJ = 'DJ'
    DM = 'DM'
    EH = 'EH'
    ET = 'ET'
    FM = 'FM'
    GD = 'GD'
    GL = 'GL'
    GM = 'GM'
    GN = 'GN'
    GQ = 'GQ'
    GW = 'GW'
    GY = 'GY'
    HT = 'HT'
    ID = 'ID'
    IN = 'IN'
    IQ = 'IQ'
    JM = 'JM'
    KG = 'KG'
    KH = 'KH'
    KI = 'KI'
    KM = 'KM'
    KN = 'KN'
    KP = 'KP'
    LA = 'LA'
    LC = 'LC'
    LR = 'LR'
    LS = 'LS'
    LY = 'LY'
    MC = 'MC'
    MD = 'MD'
    MG = 'MG'
    MK = 'MK'
    MM = 'MM'
    MR = 'MR'
    MV = 'MV'
    MW = 'MW'
    MZ = 'MZ'
    NE = 'NE'
    NG = 'NG'
    NP = 'NP'
    NR = 'NR'
    PG = 'PG'
    PW = 'PW'
    RW = 'RW'
    SB = 'SB'
    SC = 'SC'
    SD = 'SD'
    SL = 'SL'
    SM = 'SM'
    SO = 'SO'
    SR = 'SR'
    ST = 'ST'
    SY = 'SY'
    SZ = 'SZ'
    TD = 'TD'
    TG = 'TG'
    TJ = 'TJ'
    TL = 'TL'
    TM = 'TM'
    TO = 'TO'
    TV = 'TV'
    UG = 'UG'
    UZ = 'UZ'
    VA = 'VA'
    VC = 'VC'
    VU = 'VU'
    WS = 'WS'
    YE = 'YE'
    
    def __repr__(self):
        return self.value


class Currency(EnumBase, Enum):    
    
    """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""

    _ = ''
    ACU = 'ACU'
    ADP = 'ADP'
    AED = 'AED'
    AFA = 'AFA'
    ALL = 'ALL'
    AMD = 'AMD'
    ANG = 'ANG'
    AOA = 'AOA'
    AOK = 'AOK'
    AON = 'AON'
    ARA = 'ARA'
    ARS = 'ARS'
    ARZ = 'ARZ'
    ATS = 'ATS'
    AUD = 'AUD'
    AUZ = 'AUZ'
    AZM = 'AZM'
    B03 = 'B03'
    BAD = 'BAD'
    BAK = 'BAK'
    BAM = 'BAM'
    BBD = 'BBD'
    BDN = 'BDN'
    BDT = 'BDT'
    BEF = 'BEF'
    BGL = 'BGL'
    BGN = 'BGN'
    BHD = 'BHD'
    BIF = 'BIF'
    BMD = 'BMD'
    BND = 'BND'
    BR6 = 'BR6'
    BRE = 'BRE'
    BRF = 'BRF'
    BRL = 'BRL'
    BRR = 'BRR'
    BSD = 'BSD'
    BTC = 'BTC'
    BTN = 'BTN'
    BTR = 'BTR'
    BWP = 'BWP'
    BYR = 'BYR'
    BZD = 'BZD'
    C23 = 'C23'
    CAC = 'CAC'
    CAD = 'CAD'
    CAZ = 'CAZ'
    CCI = 'CCI'
    CDF = 'CDF'
    CFA = 'CFA'
    CHF = 'CHF'
    CHZ = 'CHZ'
    CLF = 'CLF'
    CLP = 'CLP'
    CLZ = 'CLZ'
    CNH = 'CNH'
    CNO = 'CNO'
    CNY = 'CNY'
    CNZ = 'CNZ'
    COP = 'COP'
    COZ = 'COZ'
    CPB = 'CPB'
    CPI = 'CPI'
    CRC = 'CRC'
    CUP = 'CUP'
    CVE = 'CVE'
    CYP = 'CYP'
    CZH = 'CZH'
    CZK = 'CZK'
    DAX = 'DAX'
    DEM = 'DEM'
    DIJ = 'DIJ'
    DJF = 'DJF'
    DKK = 'DKK'
    DOP = 'DOP'
    DZD = 'DZD'
    E51 = 'E51'
    E52 = 'E52'
    E53 = 'E53'
    E54 = 'E54'
    ECI = 'ECI'
    ECS = 'ECS'
    ECU = 'ECU'
    EEK = 'EEK'
    EF0 = 'EF0'
    EGP = 'EGP'
    ESP = 'ESP'
    ETB = 'ETB'
    EUR = 'EUR'
    EUZ = 'EUZ'
    F06 = 'F06'
    FED = 'FED'
    FIM = 'FIM'
    FJD = 'FJD'
    FKP = 'FKP'
    FRF = 'FRF'
    FT1 = 'FT1'
    GBP = 'GBP'
    GBZ = 'GBZ'
    GEK = 'GEK'
    GHC = 'GHC'
    GHS = 'GHS'
    GHY = 'GHY'
    GIP = 'GIP'
    GMD = 'GMD'
    GNF = 'GNF'
    GQE = 'GQE'
    GRD = 'GRD'
    GTQ = 'GTQ'
    GWP = 'GWP'
    GYD = 'GYD'
    HKB = 'HKB'
    HKD = 'HKD'
    HNL = 'HNL'
    HRK = 'HRK'
    HSI = 'HSI'
    HTG = 'HTG'
    HUF = 'HUF'
    IDB = 'IDB'
    IDO = 'IDO'
    IDR = 'IDR'
    IEP = 'IEP'
    IGP = 'IGP'
    ILS = 'ILS'
    INO = 'INO'
    INP = 'INP'
    INR = 'INR'
    IPA = 'IPA'
    IPX = 'IPX'
    IQD = 'IQD'
    IRR = 'IRR'
    IRS = 'IRS'
    ISI = 'ISI'
    ISK = 'ISK'
    ISO = 'ISO'
    ITL = 'ITL'
    J05 = 'J05'
    JMD = 'JMD'
    JNI = 'JNI'
    JOD = 'JOD'
    JPY = 'JPY'
    JPZ = 'JPZ'
    JZ9 = 'JZ9'
    KES = 'KES'
    KGS = 'KGS'
    KHR = 'KHR'
    KMF = 'KMF'
    KOR = 'KOR'
    KPW = 'KPW'
    KRW = 'KRW'
    KWD = 'KWD'
    KYD = 'KYD'
    KZT = 'KZT'
    LAK = 'LAK'
    LBA = 'LBA'
    LBP = 'LBP'
    LHY = 'LHY'
    LKR = 'LKR'
    LRD = 'LRD'
    LSL = 'LSL'
    LSM = 'LSM'
    LTL = 'LTL'
    LUF = 'LUF'
    LVL = 'LVL'
    LYD = 'LYD'
    MAD = 'MAD'
    MDL = 'MDL'
    MGF = 'MGF'
    MKD = 'MKD'
    MMK = 'MMK'
    MNT = 'MNT'
    MOP = 'MOP'
    MRO = 'MRO'
    MTP = 'MTP'
    MUR = 'MUR'
    MVR = 'MVR'
    MWK = 'MWK'
    MXB = 'MXB'
    MXN = 'MXN'
    MXP = 'MXP'
    MXW = 'MXW'
    MXZ = 'MXZ'
    MYO = 'MYO'
    MYR = 'MYR'
    MZM = 'MZM'
    MZN = 'MZN'
    NAD = 'NAD'
    ND3 = 'ND3'
    NGF = 'NGF'
    NGI = 'NGI'
    NGN = 'NGN'
    NIC = 'NIC'
    NLG = 'NLG'
    NOK = 'NOK'
    NOZ = 'NOZ'
    NPR = 'NPR'
    NZD = 'NZD'
    NZZ = 'NZZ'
    O08 = 'O08'
    OMR = 'OMR'
    PAB = 'PAB'
    PEI = 'PEI'
    PEN = 'PEN'
    PEZ = 'PEZ'
    PGK = 'PGK'
    PHP = 'PHP'
    PKR = 'PKR'
    PLN = 'PLN'
    PLZ = 'PLZ'
    PSI = 'PSI'
    PTE = 'PTE'
    PYG = 'PYG'
    QAR = 'QAR'
    R2K = 'R2K'
    ROL = 'ROL'
    RON = 'RON'
    RSD = 'RSD'
    RUB = 'RUB'
    RUF = 'RUF'
    RUR = 'RUR'
    RWF = 'RWF'
    SAR = 'SAR'
    SBD = 'SBD'
    SCR = 'SCR'
    SDP = 'SDP'
    SDR = 'SDR'
    SEK = 'SEK'
    SET = 'SET'
    SGD = 'SGD'
    SGS = 'SGS'
    SHP = 'SHP'
    SKK = 'SKK'
    SLL = 'SLL'
    SRG = 'SRG'
    SSI = 'SSI'
    STD = 'STD'
    SUR = 'SUR'
    SVC = 'SVC'
    SVT = 'SVT'
    SYP = 'SYP'
    SZL = 'SZL'
    T21 = 'T21'
    T51 = 'T51'
    T52 = 'T52'
    T53 = 'T53'
    T54 = 'T54'
    T55 = 'T55'
    T71 = 'T71'
    TE0 = 'TE0'
    TED = 'TED'
    TF9 = 'TF9'
    THB = 'THB'
    THO = 'THO'
    TMM = 'TMM'
    TND = 'TND'
    TNT = 'TNT'
    TOP = 'TOP'
    TPE = 'TPE'
    TPX = 'TPX'
    TRB = 'TRB'
    TRL = 'TRL'
    TRY = 'TRY'
    TRZ = 'TRZ'
    TTD = 'TTD'
    TWD = 'TWD'
    TZS = 'TZS'
    UAH = 'UAH'
    UCB = 'UCB'
    UDI = 'UDI'
    UFC = 'UFC'
    UFZ = 'UFZ'
    UGS = 'UGS'
    UGX = 'UGX'
    USB = 'USB'
    USD = 'USD'
    UVR = 'UVR'
    UYP = 'UYP'
    UYU = 'UYU'
    VAC = 'VAC'
    VEB = 'VEB'
    VEF = 'VEF'
    VES = 'VES'
    VND = 'VND'
    VUV = 'VUV'
    WST = 'WST'
    XAF = 'XAF'
    XAG = 'XAG'
    XAU = 'XAU'
    XPD = 'XPD'
    XPT = 'XPT'
    XCD = 'XCD'
    XDR = 'XDR'
    XEU = 'XEU'
    XOF = 'XOF'
    XPF = 'XPF'
    YDD = 'YDD'
    YER = 'YER'
    YUD = 'YUD'
    YUN = 'YUN'
    ZAL = 'ZAL'
    ZAR = 'ZAR'
    ZAZ = 'ZAZ'
    ZMK = 'ZMK'
    ZMW = 'ZMW'
    ZRN = 'ZRN'
    ZRZ = 'ZRZ'
    ZWD = 'ZWD'
    AUd = 'AUd'
    BWp = 'BWp'
    EUr = 'EUr'
    GBp = 'GBp'
    ILs = 'ILs'
    KWd = 'KWd'
    MWk = 'MWk'
    SGd = 'SGd'
    SZl = 'SZl'
    USd = 'USd'
    ZAr = 'ZAr'
    
    def __repr__(self):
        return self.value


class DayCountFraction(EnumBase, Enum):    
    
    """Day Count Fraction"""

    ACT_OVER_360 = 'ACT/360'
    ACT_OVER_365_Fixed = 'ACT/365 (Fixed)'
    ACT_OVER_365_ISDA = 'ACT/365 ISDA'
    ACT_OVER_ACT_ISDA = 'ACT/ACT ISDA'
    _30_OVER_360 = '30/360'
    _30E_OVER_360 = '30E/360'
    
    def __repr__(self):
        return self.value


class Format(EnumBase, Enum):    
    
    """Alternative format for data to be returned in"""

    Json = 'Json'
    Excel = 'Excel'
    MessagePack = 'MessagePack'
    Pdf = 'Pdf'
    
    def __repr__(self):
        return self.value


class Frequency(EnumBase, Enum):    
    
    """frequency"""

    Daily = 'Daily'
    Weekly = 'Weekly'
    Monthly = 'Monthly'
    Quarterly = 'Quarterly'
    Annually = 'Annually'
    
    def __repr__(self):
        return self.value


class IndexCreateSource(EnumBase, Enum):    
    
    """Source of basket create"""

    API = 'API'
    CUBE = 'CUBE'
    Hedger = 'Hedger'
    Pretrade = 'Pretrade'
    Marquee_UI = 'Marquee UI'
    Clone = 'Clone'
    
    def __repr__(self):
        return self.value


class LiquidityMeasure(EnumBase, Enum):    
    
    """A list of the different liquidity measures to choose from."""

    Summary = 'Summary'
    Constituent_Transaction_Costs = 'Constituent Transaction Costs'
    Constituents = 'Constituents'
    Largest_Holdings_By_Weight = 'Largest Holdings By Weight'
    Least_Liquid_Holdings = 'Least Liquid Holdings'
    ADV_Percent_Buckets = 'ADV Percent Buckets'
    Market_Cap_Buckets = 'Market Cap Buckets'
    Region_Buckets = 'Region Buckets'
    Country_Buckets = 'Country Buckets'
    Sector_Buckets = 'Sector Buckets'
    Industry_Buckets = 'Industry Buckets'
    Risk_Buckets = 'Risk Buckets'
    Factor_Risk_Buckets = 'Factor Risk Buckets'
    Exposure_Buckets = 'Exposure Buckets'
    Factor_Exposure_Buckets = 'Factor Exposure Buckets'
    Percent_Of_Trade_Complete_Over_Time = 'Percent Of Trade Complete Over Time'
    Execution_Cost_With_Different_Time_Horizons = 'Execution Cost With Different Time Horizons'
    Participation_Rate_With_Different_Time_Horizons = 'Participation Rate With Different Time Horizons'
    Risk_With_Different_Time_Horizons = 'Risk With Different Time Horizons'
    Historical_ADV_Percent_Curve = 'Historical ADV Percent Curve'
    Time_Series_Data = 'Time Series Data'
    
    def __repr__(self):
        return self.value


class MarketDataShockType(EnumBase, Enum):    
    
    """Market data shock type"""

    Absolute = 'Absolute'
    Proportional = 'Proportional'
    Invalid = 'Invalid'
    Override = 'Override'
    StdDev = 'StdDev'
    AutoDefault = 'AutoDefault'
    CSWFFR = 'CSWFFR'
    StdVolFactor = 'StdVolFactor'
    StdVolFactorProportional = 'StdVolFactorProportional'
    
    def __repr__(self):
        return self.value


class MarketDataVendor(EnumBase, Enum):    
    
    Goldman_Sachs = 'Goldman Sachs'
    Thomson_Reuters = 'Thomson Reuters'
    Solactive = 'Solactive'
    Bloomberg = 'Bloomberg'
    Axioma = 'Axioma'
    Goldman_Sachs_Prime_Services = 'Goldman Sachs Prime Services'
    Goldman_Sachs_Global_Investment_Research = 'Goldman Sachs Global Investment Research'
    National_Weather_Service = 'National Weather Service'
    WM = 'WM'
    Hedge_Fund_Research__Inc_ = 'Hedge Fund Research, Inc.'
    London_Stock_Exchange = 'London Stock Exchange'
    Goldman_Sachs_MDFarm = 'Goldman Sachs MDFarm'
    PredictIt = 'PredictIt'
    Iowa_Electronic_Markets = 'Iowa Electronic Markets'
    RealClearPolitics = 'RealClearPolitics'
    _538 = '538'
    Opinium = 'Opinium'
    YouGov = 'YouGov'
    Survation = 'Survation'
    Survation__YouGov = 'Survation, YouGov'
    
    def __repr__(self):
        return self.value


class OptionExpiryType(EnumBase, Enum):    
    
    _1m = '1m'
    _2m = '2m'
    _3m = '3m'
    _4m = '4m'
    _5m = '5m'
    _6m = '6m'
    
    def __repr__(self):
        return self.value


class OptionSettlementMethod(EnumBase, Enum):    
    
    """How the option is settled (e.g. Cash, Physical)"""

    Cash = 'Cash'
    Physical = 'Physical'
    
    def __repr__(self):
        return self.value


class OptionStrikeType(EnumBase, Enum):    
    
    Relative = 'Relative'
    Delta = 'Delta'
    
    def __repr__(self):
        return self.value


class OptionStyle(EnumBase, Enum):    
    
    """Option Exercise Style"""

    European = 'European'
    American = 'American'
    Bermudan = 'Bermudan'
    
    def __repr__(self):
        return self.value


class OptionType(EnumBase, Enum):    
    
    """Option Type"""

    Call = 'Call'
    Put = 'Put'
    
    def __repr__(self):
        return self.value


class PayReceive(EnumBase, Enum):    
    
    """Pay or receive fixed"""

    Pay = 'Pay'
    Receive = 'Receive'
    Straddle = 'Straddle'
    
    def __repr__(self):
        return self.value


class PricingLocation(EnumBase, Enum):    
    
    """Based on the location of the exchange. Called 'Native Region' in SecDB"""

    NYC = 'NYC'
    LDN = 'LDN'
    TKO = 'TKO'
    HKG = 'HKG'
    
    def __repr__(self):
        return self.value


class Region(EnumBase, Enum):    
    
    """Regional classification for the asset"""

    _ = ''
    Americas = 'Americas'
    Asia = 'Asia'
    EM = 'EM'
    Europe = 'Europe'
    Global = 'Global'
    
    def __repr__(self):
        return self.value


class RiskMeasureType(EnumBase, Enum):    
    
    """The type of measure to perform risk on. e.g. Greeks"""

    Annual_ATMF_Implied_Volatility = 'Annual ATMF Implied Volatility'
    Annual_Implied_Volatility = 'Annual Implied Volatility'
    AnnuityLocalCcy = 'AnnuityLocalCcy'
    Basis = 'Basis'
    CRIF_IRCurve = 'CRIF IRCurve'
    Daily_Implied_Volatility = 'Daily Implied Volatility'
    Delta = 'Delta'
    DeltaLocalCcy = 'DeltaLocalCcy'
    DeltaCrossCcy = 'DeltaCrossCcy'
    Dollar_Price = 'Dollar Price'
    DV01 = 'DV01'
    FairVarStrike = 'FairVarStrike'
    FairVolStrike = 'FairVolStrike'
    Forward_Price = 'Forward Price'
    Forward_Rate = 'Forward Rate'
    Price = 'Price'
    Gamma = 'Gamma'
    GammaLocalCcy = 'GammaLocalCcy'
    InflationDelta = 'InflationDelta'
    Local_Currency_Accrual_in_Cents = 'Local Currency Accrual in Cents'
    Local_Currency_Annuity = 'Local Currency Annuity'
    OAS = 'OAS'
    ParallelBasis = 'ParallelBasis'
    ParallelDelta = 'ParallelDelta'
    ParallelDeltaLocalCcy = 'ParallelDeltaLocalCcy'
    ParallelDeltaCrossCcy = 'ParallelDeltaCrossCcy'
    ParallelInflationDelta = 'ParallelInflationDelta'
    ParallelInflationDeltaLocalCcy = 'ParallelInflationDeltaLocalCcy'
    ParallelGamma = 'ParallelGamma'
    ParallelGammaLocalCcy = 'ParallelGammaLocalCcy'
    ParallelVega = 'ParallelVega'
    ParallelVegaLocalCcy = 'ParallelVegaLocalCcy'
    Premium_In_Cents = 'Premium In Cents'
    Resolved_Instrument_Values = 'Resolved Instrument Values'
    PNL = 'PNL'
    PV = 'PV'
    Spot = 'Spot'
    Spot_Rate = 'Spot Rate'
    Theta = 'Theta'
    Vanna = 'Vanna'
    Vega = 'Vega'
    VegaLocalCcy = 'VegaLocalCcy'
    Volga = 'Volga'
    MV = 'MV'
    
    def __repr__(self):
        return self.value


class RiskMeasureUnit(EnumBase, Enum):    
    
    """The unit of change of underlying in the risk computation."""

    Percent = 'Percent'
    Dollar = 'Dollar'
    BPS = 'BPS'
    
    def __repr__(self):
        return self.value


class RiskModelVendor(EnumBase, Enum):    
    
    Axioma = 'Axioma'
    
    def __repr__(self):
        return self.value


class StrikeMethodType(EnumBase, Enum):    
    
    Spread = 'Spread'
    Delta = 'Delta'
    Percentage_of_Price = 'Percentage of Price'
    Fixed = 'Fixed'
    
    def __repr__(self):
        return self.value


class SwapClearingHouse(EnumBase, Enum):    
    
    """Swap Clearing House"""

    LCH = 'LCH'
    EUREX = 'EUREX'
    JSCC = 'JSCC'
    CME = 'CME'
    
    def __repr__(self):
        return self.value


class SwapSettlement(EnumBase, Enum):    
    
    """Swap Settlement Type"""

    Phys_CLEARED = 'Phys.CLEARED'
    Physical = 'Physical'
    Cash_CollatCash = 'Cash.CollatCash'
    Cash_PYU = 'Cash.PYU'
    
    def __repr__(self):
        return self.value


class TradeType(EnumBase, Enum):    
    
    """Direction"""

    Buy = 'Buy'
    Sell = 'Sell'
    
    def __repr__(self):
        return self.value


class UnderlierType(EnumBase, Enum):    
    
    """Type of underlyer"""

    BBID = 'BBID'
    CUSIP = 'CUSIP'
    ISIN = 'ISIN'
    SEDOL = 'SEDOL'
    RIC = 'RIC'
    Ticker = 'Ticker'
    
    def __repr__(self):
        return self.value


class ValuationTime(EnumBase, Enum):    
    
    """The time of valuation, e.g. for an option"""

    MktClose = 'MktClose'
    MktOpen = 'MktOpen'
    SQ = 'SQ'
    
    def __repr__(self):
        return self.value


class VarianceConvention(EnumBase, Enum):    
    
    """Specifies whether the variance is Annualized or Total"""

    Annualized = 'Annualized'
    Total = 'Total'
    
    def __repr__(self):
        return self.value


class AssetIdPriceable(Priceable):
        
    """An object to hold assetId when it can't be passed as a string."""

    @camel_case_translate
    def __init__(
        self,
        asset_id: str = None,
        name: str = None
    ):        
        super().__init__()
        self.asset_id = asset_id
        self.name = name

    @property
    def asset_id(self) -> str:
        """Marquee unique asset identifier."""
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: str):
        self._property_changed('asset_id')
        self.__asset_id = value        


class CSLDate(Base):
        
    """A date"""

    @camel_case_translate
    def __init__(
        self,
        date_value: datetime.date = None,
        name: str = None
    ):        
        super().__init__()
        self.date_value = date_value
        self.name = name

    @property
    def date_value(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__date_value

    @date_value.setter
    def date_value(self, value: datetime.date):
        self._property_changed('date_value')
        self.__date_value = value        


class CSLDouble(Base):
        
    """A double"""

    @camel_case_translate
    def __init__(
        self,
        double_value: float = None,
        name: str = None
    ):        
        super().__init__()
        self.double_value = double_value
        self.name = name

    @property
    def double_value(self) -> float:
        """The value"""
        return self.__double_value

    @double_value.setter
    def double_value(self, value: float):
        self._property_changed('double_value')
        self.__double_value = value        


class CSLFXCross(Base):
        
    """An FX cross"""

    @camel_case_translate
    def __init__(
        self,
        string_value: str = None,
        name: str = None
    ):        
        super().__init__()
        self.string_value = string_value
        self.name = name

    @property
    def string_value(self) -> str:
        """Currency pair"""
        return self.__string_value

    @string_value.setter
    def string_value(self, value: str):
        self._property_changed('string_value')
        self.__string_value = value        


class CSLIndex(Base):
        
    """An index"""

    @camel_case_translate
    def __init__(
        self,
        string_value: str = None,
        name: str = None
    ):        
        super().__init__()
        self.string_value = string_value
        self.name = name

    @property
    def string_value(self) -> str:
        """Display name of the asset"""
        return self.__string_value

    @string_value.setter
    def string_value(self, value: str):
        self._property_changed('string_value')
        self.__string_value = value        


class CSLSimpleSchedule(Base):
        
    """A fixing date, settlement date pair"""

    @camel_case_translate
    def __init__(
        self,
        fixing_date: datetime.date = None,
        settlement_date: datetime.date = None,
        name: str = None
    ):        
        super().__init__()
        self.fixing_date = fixing_date
        self.settlement_date = settlement_date
        self.name = name

    @property
    def fixing_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__fixing_date

    @fixing_date.setter
    def fixing_date(self, value: datetime.date):
        self._property_changed('fixing_date')
        self.__fixing_date = value        

    @property
    def settlement_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__settlement_date

    @settlement_date.setter
    def settlement_date(self, value: datetime.date):
        self._property_changed('settlement_date')
        self.__settlement_date = value        


class CSLStock(Base):
        
    """A stock"""

    @camel_case_translate
    def __init__(
        self,
        string_value: str = None,
        name: str = None
    ):        
        super().__init__()
        self.string_value = string_value
        self.name = name

    @property
    def string_value(self) -> str:
        """Display name of the asset"""
        return self.__string_value

    @string_value.setter
    def string_value(self, value: str):
        self._property_changed('string_value')
        self.__string_value = value        


class CSLString(Base):
        
    """A string"""

    @camel_case_translate
    def __init__(
        self,
        string_value: str = None,
        name: str = None
    ):        
        super().__init__()
        self.string_value = string_value
        self.name = name

    @property
    def string_value(self) -> str:
        """The value"""
        return self.__string_value

    @string_value.setter
    def string_value(self, value: str):
        self._property_changed('string_value')
        self.__string_value = value        


class CSLSymCaseNamedParam(Base):
        
    """A named case-sensitive string."""

    @camel_case_translate
    def __init__(
        self,
        sym_case_value: str = None,
        name: str = None
    ):        
        super().__init__()
        self.sym_case_value = sym_case_value
        self.name = name

    @property
    def sym_case_value(self) -> str:
        """A case-sensitive string"""
        return self.__sym_case_value

    @sym_case_value.setter
    def sym_case_value(self, value: str):
        self._property_changed('sym_case_value')
        self.__sym_case_value = value        

    @property
    def name(self) -> str:
        """A name for the symbol"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        


class CarryScenario(Scenario):
        
    """A scenario to manipulate time along the forward curve"""

    @camel_case_translate
    def __init__(
        self,
        time_shift: int = None,
        roll_to_fwds: bool = True,
        name: str = None
    ):        
        super().__init__()
        self.time_shift = time_shift
        self.roll_to_fwds = roll_to_fwds
        self.name = name

    @property
    def scenario_type(self) -> str:
        """CarryScenario"""
        return 'CarryScenario'        

    @property
    def time_shift(self) -> int:
        """Number of days to shift market (in days)"""
        return self.__time_shift

    @time_shift.setter
    def time_shift(self, value: int):
        self._property_changed('time_shift')
        self.__time_shift = value        

    @property
    def roll_to_fwds(self) -> bool:
        """Roll along the forward curve or roll in spot space"""
        return self.__roll_to_fwds

    @roll_to_fwds.setter
    def roll_to_fwds(self, value: bool):
        self._property_changed('roll_to_fwds')
        self.__roll_to_fwds = value        


class DateRange(Base):
        
    @camel_case_translate
    def __init__(
        self,
        end_date: datetime.date = None,
        start_date: datetime.date = None,
        name: str = None
    ):        
        super().__init__()
        self.end_date = end_date
        self.start_date = start_date
        self.name = name

    @property
    def end_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__end_date

    @end_date.setter
    def end_date(self, value: datetime.date):
        self._property_changed('end_date')
        self.__end_date = value        

    @property
    def start_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__start_date

    @start_date.setter
    def start_date(self, value: datetime.date):
        self._property_changed('start_date')
        self.__start_date = value        


class EntitlementExclusions(Base):
        
    """Defines the exclusion entitlements of a given resource"""

    @camel_case_translate
    def __init__(
        self,
        view: Tuple[Tuple[str, ...], ...] = None,
        edit: Tuple[Tuple[str, ...], ...] = None,
        admin: Tuple[Tuple[str, ...], ...] = None,
        rebalance: Tuple[Tuple[str, ...], ...] = None,
        trade: Tuple[Tuple[str, ...], ...] = None,
        upload: Tuple[Tuple[str, ...], ...] = None,
        query: Tuple[Tuple[str, ...], ...] = None,
        performance_details: Tuple[Tuple[str, ...], ...] = None,
        plot: Tuple[Tuple[str, ...], ...] = None,
        delete: Tuple[Tuple[str, ...], ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.view = view
        self.edit = edit
        self.admin = admin
        self.rebalance = rebalance
        self.trade = trade
        self.upload = upload
        self.query = query
        self.performance_details = performance_details
        self.plot = plot
        self.delete = delete
        self.name = name

    @property
    def view(self) -> Tuple[Tuple[str, ...], ...]:
        return self.__view

    @view.setter
    def view(self, value: Tuple[Tuple[str, ...], ...]):
        self._property_changed('view')
        self.__view = value        

    @property
    def edit(self) -> Tuple[Tuple[str, ...], ...]:
        return self.__edit

    @edit.setter
    def edit(self, value: Tuple[Tuple[str, ...], ...]):
        self._property_changed('edit')
        self.__edit = value        

    @property
    def admin(self) -> Tuple[Tuple[str, ...], ...]:
        return self.__admin

    @admin.setter
    def admin(self, value: Tuple[Tuple[str, ...], ...]):
        self._property_changed('admin')
        self.__admin = value        

    @property
    def rebalance(self) -> Tuple[Tuple[str, ...], ...]:
        return self.__rebalance

    @rebalance.setter
    def rebalance(self, value: Tuple[Tuple[str, ...], ...]):
        self._property_changed('rebalance')
        self.__rebalance = value        

    @property
    def trade(self) -> Tuple[Tuple[str, ...], ...]:
        return self.__trade

    @trade.setter
    def trade(self, value: Tuple[Tuple[str, ...], ...]):
        self._property_changed('trade')
        self.__trade = value        

    @property
    def upload(self) -> Tuple[Tuple[str, ...], ...]:
        return self.__upload

    @upload.setter
    def upload(self, value: Tuple[Tuple[str, ...], ...]):
        self._property_changed('upload')
        self.__upload = value        

    @property
    def query(self) -> Tuple[Tuple[str, ...], ...]:
        return self.__query

    @query.setter
    def query(self, value: Tuple[Tuple[str, ...], ...]):
        self._property_changed('query')
        self.__query = value        

    @property
    def performance_details(self) -> Tuple[Tuple[str, ...], ...]:
        return self.__performance_details

    @performance_details.setter
    def performance_details(self, value: Tuple[Tuple[str, ...], ...]):
        self._property_changed('performance_details')
        self.__performance_details = value        

    @property
    def plot(self) -> Tuple[Tuple[str, ...], ...]:
        return self.__plot

    @plot.setter
    def plot(self, value: Tuple[Tuple[str, ...], ...]):
        self._property_changed('plot')
        self.__plot = value        

    @property
    def delete(self) -> Tuple[Tuple[str, ...], ...]:
        return self.__delete

    @delete.setter
    def delete(self, value: Tuple[Tuple[str, ...], ...]):
        self._property_changed('delete')
        self.__delete = value        


class Entitlements(Base):
        
    """Defines the entitlements of a given resource"""

    @camel_case_translate
    def __init__(
        self,
        view: Tuple[str, ...] = None,
        edit: Tuple[str, ...] = None,
        admin: Tuple[str, ...] = None,
        rebalance: Tuple[str, ...] = None,
        trade: Tuple[str, ...] = None,
        upload: Tuple[str, ...] = None,
        query: Tuple[str, ...] = None,
        performance_details: Tuple[str, ...] = None,
        plot: Tuple[str, ...] = None,
        delete: Tuple[str, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.view = view
        self.edit = edit
        self.admin = admin
        self.rebalance = rebalance
        self.trade = trade
        self.upload = upload
        self.query = query
        self.performance_details = performance_details
        self.plot = plot
        self.delete = delete
        self.name = name

    @property
    def view(self) -> Tuple[str, ...]:
        """Permission to view the resource and its contents"""
        return self.__view

    @view.setter
    def view(self, value: Tuple[str, ...]):
        self._property_changed('view')
        self.__view = value        

    @property
    def edit(self) -> Tuple[str, ...]:
        """Permission to edit details about the resource content, excluding entitlements.
           Can also delete the resource"""
        return self.__edit

    @edit.setter
    def edit(self, value: Tuple[str, ...]):
        self._property_changed('edit')
        self.__edit = value        

    @property
    def admin(self) -> Tuple[str, ...]:
        """Permission to edit all details of the resource, including entitlements. Can also
           delete the resource"""
        return self.__admin

    @admin.setter
    def admin(self, value: Tuple[str, ...]):
        self._property_changed('admin')
        self.__admin = value        

    @property
    def rebalance(self) -> Tuple[str, ...]:
        """Permission to rebalance the constituent weights of the resource"""
        return self.__rebalance

    @rebalance.setter
    def rebalance(self, value: Tuple[str, ...]):
        self._property_changed('rebalance')
        self.__rebalance = value        

    @property
    def trade(self) -> Tuple[str, ...]:
        """Permission to trade the resource"""
        return self.__trade

    @trade.setter
    def trade(self, value: Tuple[str, ...]):
        self._property_changed('trade')
        self.__trade = value        

    @property
    def upload(self) -> Tuple[str, ...]:
        """Permission to upload data to the given resource"""
        return self.__upload

    @upload.setter
    def upload(self, value: Tuple[str, ...]):
        self._property_changed('upload')
        self.__upload = value        

    @property
    def query(self) -> Tuple[str, ...]:
        """Permission to query data from the given resource"""
        return self.__query

    @query.setter
    def query(self, value: Tuple[str, ...]):
        self._property_changed('query')
        self.__query = value        

    @property
    def performance_details(self) -> Tuple[str, ...]:
        """Permission to view the resource, it's entire contents, and related data"""
        return self.__performance_details

    @performance_details.setter
    def performance_details(self, value: Tuple[str, ...]):
        self._property_changed('performance_details')
        self.__performance_details = value        

    @property
    def plot(self) -> Tuple[str, ...]:
        """Permission to plot data from the given resource"""
        return self.__plot

    @plot.setter
    def plot(self, value: Tuple[str, ...]):
        self._property_changed('plot')
        self.__plot = value        

    @property
    def delete(self) -> Tuple[str, ...]:
        """Permission to delete the resource"""
        return self.__delete

    @delete.setter
    def delete(self, value: Tuple[str, ...]):
        self._property_changed('delete')
        self.__delete = value        


class ISelectNewUnit(Base):
        
    @camel_case_translate
    def __init__(
        self,
        id_: str,
        new_units: float = None,
        name: str = None
    ):        
        super().__init__()
        self.__id = id_
        self.new_units = new_units
        self.name = name

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def new_units(self) -> float:
        return self.__new_units

    @new_units.setter
    def new_units(self, value: float):
        self._property_changed('new_units')
        self.__new_units = value        


class ISelectNewWeight(Base):
        
    @camel_case_translate
    def __init__(
        self,
        id_: str,
        new_weight: float = None,
        name: str = None
    ):        
        super().__init__()
        self.__id = id_
        self.new_weight = new_weight
        self.name = name

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def new_weight(self) -> float:
        return self.__new_weight

    @new_weight.setter
    def new_weight(self, value: float):
        self._property_changed('new_weight')
        self.__new_weight = value        


class Identifier(Base):
        
    @camel_case_translate
    def __init__(
        self,
        type_: str = None,
        value: str = None,
        name: str = None
    ):        
        super().__init__()
        self.__type = type_
        self.value = value
        self.name = name

    @property
    def type(self) -> str:
        """Identifier type code"""
        return self.__type

    @type.setter
    def type(self, value: str):
        self._property_changed('type')
        self.__type = value        

    @property
    def value(self) -> str:
        """Identifier value"""
        return self.__value

    @value.setter
    def value(self, value: str):
        self._property_changed('value')
        self.__value = value        


class Link(Base):
        
    """Hyperlink"""

    @camel_case_translate
    def __init__(
        self,
        title: str = None,
        source: str = None,
        name: str = None
    ):        
        super().__init__()
        self.title = title
        self.source = source
        self.name = name

    @property
    def title(self) -> str:
        """display text"""
        return self.__title

    @title.setter
    def title(self, value: str):
        self._property_changed('title')
        self.__title = value        

    @property
    def source(self) -> str:
        """link"""
        return self.__source

    @source.setter
    def source(self, value: str):
        self._property_changed('source')
        self.__source = value        


class LiquidityReportParameters(Base):
        
    """Parameters to be used on liquidity reports"""

    @camel_case_translate
    def __init__(
        self,
        title: str = None,
        email: str = None,
        trading_desk: str = None,
        name: str = None
    ):        
        super().__init__()
        self.title = title
        self.email = email
        self.trading_desk = trading_desk
        self.name = name

    @property
    def title(self) -> str:
        """Report title"""
        return self.__title

    @title.setter
    def title(self, value: str):
        self._property_changed('title')
        self.__title = value        

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value: str):
        self._property_changed('email')
        self.__email = value        

    @property
    def trading_desk(self) -> str:
        return self.__trading_desk

    @trading_desk.setter
    def trading_desk(self, value: str):
        self._property_changed('trading_desk')
        self.__trading_desk = value        


class MarketDataTypeAndAsset(Base):
        
    """Market data type and asset, e.g. type=IR, asset=USD"""

    @camel_case_translate
    def __init__(
        self,
        type_: str,
        asset: str,
        name: str = None
    ):        
        super().__init__()
        self.__type = type_
        self.asset = asset
        self.name = name

    @property
    def type(self) -> str:
        """Market data type, e.g., IR, IR Vol, Eq etc"""
        return self.__type

    @type.setter
    def type(self, value: str):
        self._property_changed('type')
        self.__type = value        

    @property
    def asset(self) -> str:
        """Market data asset, e.g., USD, USD-LIBOR-BBA etc"""
        return self.__asset

    @asset.setter
    def asset(self, value: str):
        self._property_changed('asset')
        self.__asset = value        


class Op(Base):
        
    """Operations for searches."""

    @camel_case_translate
    def __init__(
        self,
        gte: Union[datetime.date, float] = None,
        lte: Union[datetime.date, float] = None,
        lt: Union[datetime.date, float] = None,
        gt: Union[datetime.date, float] = None,
        name: str = None
    ):        
        super().__init__()
        self.gte = gte
        self.lte = lte
        self.lt = lt
        self.gt = gt
        self.name = name

    @property
    def gte(self) -> Union[datetime.date, float]:
        """search for values greater than or equal."""
        return self.__gte

    @gte.setter
    def gte(self, value: Union[datetime.date, float]):
        self._property_changed('gte')
        self.__gte = value        

    @property
    def lte(self) -> Union[datetime.date, float]:
        """search for values less than or equal to."""
        return self.__lte

    @lte.setter
    def lte(self, value: Union[datetime.date, float]):
        self._property_changed('lte')
        self.__lte = value        

    @property
    def lt(self) -> Union[datetime.date, float]:
        """search for values less than."""
        return self.__lt

    @lt.setter
    def lt(self, value: Union[datetime.date, float]):
        self._property_changed('lt')
        self.__lt = value        

    @property
    def gt(self) -> Union[datetime.date, float]:
        """search for values greater than."""
        return self.__gt

    @gt.setter
    def gt(self, value: Union[datetime.date, float]):
        self._property_changed('gt')
        self.__gt = value        


class PerformanceStats(Base):
        
    """Performance statistics."""

    @camel_case_translate
    def __init__(
        self,
        alpha: float = None,
        annualized_return: float = None,
        annualized_volatility: float = None,
        average_return: float = None,
        average_value: float = None,
        average_volume_last_month: float = None,
        best_month: float = None,
        best_month_date: datetime.date = None,
        beta: float = None,
        close_price: float = None,
        correlation: float = None,
        current_value: float = None,
        drawdown_over_return: float = None,
        high: float = None,
        high_eod: float = None,
        last_change: float = None,
        last_change_pct: float = None,
        last_date: datetime.date = None,
        last_value: float = None,
        low: float = None,
        low_eod: float = None,
        max_draw_down: float = None,
        max_draw_down_duration: int = None,
        open_price: float = None,
        positive_months: float = None,
        sharpe_ratio: float = None,
        sortino_ratio: float = None,
        worst_month: float = None,
        worst_month_date: datetime.date = None,
        total_return: float = None,
        volume: float = None,
        name: str = None
    ):        
        super().__init__()
        self.alpha = alpha
        self.annualized_return = annualized_return
        self.annualized_volatility = annualized_volatility
        self.average_return = average_return
        self.average_value = average_value
        self.average_volume_last_month = average_volume_last_month
        self.best_month = best_month
        self.best_month_date = best_month_date
        self.beta = beta
        self.close_price = close_price
        self.correlation = correlation
        self.current_value = current_value
        self.drawdown_over_return = drawdown_over_return
        self.high = high
        self.high_eod = high_eod
        self.last_change = last_change
        self.last_change_pct = last_change_pct
        self.last_date = last_date
        self.last_value = last_value
        self.low = low
        self.low_eod = low_eod
        self.max_draw_down = max_draw_down
        self.max_draw_down_duration = max_draw_down_duration
        self.open_price = open_price
        self.positive_months = positive_months
        self.sharpe_ratio = sharpe_ratio
        self.sortino_ratio = sortino_ratio
        self.worst_month = worst_month
        self.worst_month_date = worst_month_date
        self.total_return = total_return
        self.volume = volume
        self.name = name

    @property
    def alpha(self) -> float:
        """Measure of performance compared to a market benchmark."""
        return self.__alpha

    @alpha.setter
    def alpha(self, value: float):
        self._property_changed('alpha')
        self.__alpha = value        

    @property
    def annualized_return(self) -> float:
        """Compounded Annual Growth Rate (CAGR)."""
        return self.__annualized_return

    @annualized_return.setter
    def annualized_return(self, value: float):
        self._property_changed('annualized_return')
        self.__annualized_return = value        

    @property
    def annualized_volatility(self) -> float:
        """Standard deviation of daily returns, annualized."""
        return self.__annualized_volatility

    @annualized_volatility.setter
    def annualized_volatility(self, value: float):
        self._property_changed('annualized_volatility')
        self.__annualized_volatility = value        

    @property
    def average_return(self) -> float:
        """Average of the performance returns."""
        return self.__average_return

    @average_return.setter
    def average_return(self, value: float):
        self._property_changed('average_return')
        self.__average_return = value        

    @property
    def average_value(self) -> float:
        """Average value."""
        return self.__average_value

    @average_value.setter
    def average_value(self, value: float):
        self._property_changed('average_value')
        self.__average_value = value        

    @property
    def average_volume_last_month(self) -> float:
        """30 day average volume."""
        return self.__average_volume_last_month

    @average_volume_last_month.setter
    def average_volume_last_month(self, value: float):
        self._property_changed('average_volume_last_month')
        self.__average_volume_last_month = value        

    @property
    def best_month(self) -> float:
        """Best monthly return (first to last day of month)."""
        return self.__best_month

    @best_month.setter
    def best_month(self, value: float):
        self._property_changed('best_month')
        self.__best_month = value        

    @property
    def best_month_date(self) -> datetime.date:
        """Best monthly return date (first to last day of month)."""
        return self.__best_month_date

    @best_month_date.setter
    def best_month_date(self, value: datetime.date):
        self._property_changed('best_month_date')
        self.__best_month_date = value        

    @property
    def beta(self) -> float:
        """Measure of volatility compared to a market benchmark."""
        return self.__beta

    @beta.setter
    def beta(self, value: float):
        self._property_changed('beta')
        self.__beta = value        

    @property
    def close_price(self) -> float:
        """previous close price."""
        return self.__close_price

    @close_price.setter
    def close_price(self, value: float):
        self._property_changed('close_price')
        self.__close_price = value        

    @property
    def correlation(self) -> float:
        """Pearson correlation."""
        return self.__correlation

    @correlation.setter
    def correlation(self, value: float):
        self._property_changed('correlation')
        self.__correlation = value        

    @property
    def current_value(self) -> float:
        """Current value."""
        return self.__current_value

    @current_value.setter
    def current_value(self, value: float):
        self._property_changed('current_value')
        self.__current_value = value        

    @property
    def drawdown_over_return(self) -> float:
        """Maximum drawdown divided by annualized return."""
        return self.__drawdown_over_return

    @drawdown_over_return.setter
    def drawdown_over_return(self, value: float):
        self._property_changed('drawdown_over_return')
        self.__drawdown_over_return = value        

    @property
    def high(self) -> float:
        """Highest real time price for the previous 24 hours."""
        return self.__high

    @high.setter
    def high(self, value: float):
        self._property_changed('high')
        self.__high = value        

    @property
    def high_eod(self) -> float:
        """Highest end of day price."""
        return self.__high_eod

    @high_eod.setter
    def high_eod(self, value: float):
        self._property_changed('high_eod')
        self.__high_eod = value        

    @property
    def last_change(self) -> float:
        """Last published value."""
        return self.__last_change

    @last_change.setter
    def last_change(self, value: float):
        self._property_changed('last_change')
        self.__last_change = value        

    @property
    def last_change_pct(self) -> float:
        """Last change in percent."""
        return self.__last_change_pct

    @last_change_pct.setter
    def last_change_pct(self, value: float):
        self._property_changed('last_change_pct')
        self.__last_change_pct = value        

    @property
    def last_date(self) -> datetime.date:
        """Last publication date."""
        return self.__last_date

    @last_date.setter
    def last_date(self, value: datetime.date):
        self._property_changed('last_date')
        self.__last_date = value        

    @property
    def last_value(self) -> float:
        """Last published value."""
        return self.__last_value

    @last_value.setter
    def last_value(self, value: float):
        self._property_changed('last_value')
        self.__last_value = value        

    @property
    def low(self) -> float:
        """Lowest real time price for the previous 24 hours."""
        return self.__low

    @low.setter
    def low(self, value: float):
        self._property_changed('low')
        self.__low = value        

    @property
    def low_eod(self) -> float:
        """Lowest end of day price."""
        return self.__low_eod

    @low_eod.setter
    def low_eod(self, value: float):
        self._property_changed('low_eod')
        self.__low_eod = value        

    @property
    def max_draw_down(self) -> float:
        """Maximum peak to trough percentage drawdown."""
        return self.__max_draw_down

    @max_draw_down.setter
    def max_draw_down(self, value: float):
        self._property_changed('max_draw_down')
        self.__max_draw_down = value        

    @property
    def max_draw_down_duration(self) -> int:
        """Amount of time in days between beginning and end of drawdown."""
        return self.__max_draw_down_duration

    @max_draw_down_duration.setter
    def max_draw_down_duration(self, value: int):
        self._property_changed('max_draw_down_duration')
        self.__max_draw_down_duration = value        

    @property
    def open_price(self) -> float:
        """Open price."""
        return self.__open_price

    @open_price.setter
    def open_price(self, value: float):
        self._property_changed('open_price')
        self.__open_price = value        

    @property
    def positive_months(self) -> float:
        """Percentage of months that performed positively."""
        return self.__positive_months

    @positive_months.setter
    def positive_months(self, value: float):
        self._property_changed('positive_months')
        self.__positive_months = value        

    @property
    def sharpe_ratio(self) -> float:
        """Annualized return of the series minus risk free rate (accrued daily) divided by
           annual volatility."""
        return self.__sharpe_ratio

    @sharpe_ratio.setter
    def sharpe_ratio(self, value: float):
        self._property_changed('sharpe_ratio')
        self.__sharpe_ratio = value        

    @property
    def sortino_ratio(self) -> float:
        """Annualized return of the series minus risk free rate (accrued daily) divided by
           annual volatility of negative returns."""
        return self.__sortino_ratio

    @sortino_ratio.setter
    def sortino_ratio(self, value: float):
        self._property_changed('sortino_ratio')
        self.__sortino_ratio = value        

    @property
    def worst_month(self) -> float:
        """Worst monthly return (first to last day of month)."""
        return self.__worst_month

    @worst_month.setter
    def worst_month(self, value: float):
        self._property_changed('worst_month')
        self.__worst_month = value        

    @property
    def worst_month_date(self) -> datetime.date:
        """Worst monthly return date (first to last day of month)."""
        return self.__worst_month_date

    @worst_month_date.setter
    def worst_month_date(self, value: datetime.date):
        self._property_changed('worst_month_date')
        self.__worst_month_date = value        

    @property
    def total_return(self) -> float:
        """Total return."""
        return self.__total_return

    @total_return.setter
    def total_return(self, value: float):
        self._property_changed('total_return')
        self.__total_return = value        

    @property
    def volume(self) -> float:
        """volume."""
        return self.__volume

    @volume.setter
    def volume(self, value: float):
        self._property_changed('volume')
        self.__volume = value        


class PricingDateAndMarketDataAsOf(Base):
        
    """Pricing date and market data as of (date or time)"""

    @camel_case_translate
    def __init__(
        self,
        pricing_date: datetime.date,
        market_data_as_of: Union[datetime.date, datetime.datetime],
        name: str = None
    ):        
        super().__init__()
        self.pricing_date = pricing_date
        self.market_data_as_of = market_data_as_of
        self.name = name

    @property
    def pricing_date(self) -> datetime.date:
        """The date for which to perform the calculation"""
        return self.__pricing_date

    @pricing_date.setter
    def pricing_date(self, value: datetime.date):
        self._property_changed('pricing_date')
        self.__pricing_date = value        

    @property
    def market_data_as_of(self) -> Union[datetime.date, datetime.datetime]:
        """The date or time to source market data"""
        return self.__market_data_as_of

    @market_data_as_of.setter
    def market_data_as_of(self, value: Union[datetime.date, datetime.datetime]):
        self._property_changed('market_data_as_of')
        self.__market_data_as_of = value        


class RiskRequestParameters(Base):
        
    """Parameters for the risk request"""

    @camel_case_translate
    def __init__(
        self,
        csa_term: str = None,
        name: str = None
    ):        
        super().__init__()
        self.csa_term = csa_term
        self.name = name

    @property
    def csa_term(self) -> str:
        """The CSA Term for CSA specific discounting, e.g. EUR-1"""
        return self.__csa_term

    @csa_term.setter
    def csa_term(self, value: str):
        self._property_changed('csa_term')
        self.__csa_term = value        


class SimpleParty(Base):
        
    @camel_case_translate
    def __init__(
        self,
        party_type: str = None,
        party_name: str = None,
        name: str = None
    ):        
        super().__init__()
        self.party_type = party_type
        self.party_name = party_name
        self.name = name

    @property
    def party_type(self) -> str:
        return self.__party_type

    @party_type.setter
    def party_type(self, value: str):
        self._property_changed('party_type')
        self.__party_type = value        

    @property
    def party_name(self) -> str:
        return self.__party_name

    @party_name.setter
    def party_name(self, value: str):
        self._property_changed('party_name')
        self.__party_name = value        


class WeightedPosition(Base):
        
    @camel_case_translate
    def __init__(
        self,
        asset_id: str,
        weight: float,
        name: str = None
    ):        
        super().__init__()
        self.asset_id = asset_id
        self.weight = weight
        self.name = name

    @property
    def asset_id(self) -> str:
        """Marquee unique identifier"""
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: str):
        self._property_changed('asset_id')
        self.__asset_id = value        

    @property
    def weight(self) -> float:
        """Relative net weight of the given position"""
        return self.__weight

    @weight.setter
    def weight(self, value: float):
        self._property_changed('weight')
        self.__weight = value        


class XRef(Priceable):
        
    @camel_case_translate
    def __init__(
        self,
        ric: str = None,
        rcic: str = None,
        eid: str = None,
        gsideid: str = None,
        gsid: str = None,
        cid: str = None,
        bbid: str = None,
        bcid: str = None,
        delisted: str = None,
        bbid_equivalent: str = None,
        cusip: str = None,
        gss: str = None,
        isin: str = None,
        jsn: str = None,
        prime_id: str = None,
        sedol: str = None,
        ticker: str = None,
        valoren: str = None,
        wpk: str = None,
        gsn: str = None,
        sec_name: str = None,
        cross: str = None,
        simon_id: str = None,
        em_id: str = None,
        cm_id: str = None,
        lms_id: str = None,
        mdapi: str = None,
        mdapi_class: str = None,
        mic: str = None,
        sf_id: str = None,
        dollar_cross: str = None,
        mq_symbol: str = None,
        primary_country_ric: str = None,
        pnode_id: str = None,
        name: str = None
    ):        
        super().__init__()
        self.ric = ric
        self.rcic = rcic
        self.eid = eid
        self.gsideid = gsideid
        self.gsid = gsid
        self.cid = cid
        self.bbid = bbid
        self.bcid = bcid
        self.delisted = delisted
        self.bbid_equivalent = bbid_equivalent
        self.cusip = cusip
        self.gss = gss
        self.isin = isin
        self.jsn = jsn
        self.prime_id = prime_id
        self.sedol = sedol
        self.ticker = ticker
        self.valoren = valoren
        self.wpk = wpk
        self.gsn = gsn
        self.sec_name = sec_name
        self.cross = cross
        self.simon_id = simon_id
        self.em_id = em_id
        self.cm_id = cm_id
        self.lms_id = lms_id
        self.mdapi = mdapi
        self.mdapi_class = mdapi_class
        self.mic = mic
        self.sf_id = sf_id
        self.dollar_cross = dollar_cross
        self.mq_symbol = mq_symbol
        self.primary_country_ric = primary_country_ric
        self.pnode_id = pnode_id
        self.name = name

    @property
    def ric(self) -> str:
        """Reuters Instrument Code identifier"""
        return self.__ric

    @ric.setter
    def ric(self, value: str):
        self._property_changed('ric')
        self.__ric = value        

    @property
    def rcic(self) -> str:
        """Reuters Composite Instrument Code Identifier"""
        return self.__rcic

    @rcic.setter
    def rcic(self, value: str):
        self._property_changed('rcic')
        self.__rcic = value        

    @property
    def eid(self) -> str:
        """EID Identifier"""
        return self.__eid

    @eid.setter
    def eid(self, value: str):
        self._property_changed('eid')
        self.__eid = value        

    @property
    def gsideid(self) -> str:
        """GSID_EID Identifier"""
        return self.__gsideid

    @gsideid.setter
    def gsideid(self, value: str):
        self._property_changed('gsideid')
        self.__gsideid = value        

    @property
    def gsid(self) -> str:
        """GSID Identifier"""
        return self.__gsid

    @gsid.setter
    def gsid(self, value: str):
        self._property_changed('gsid')
        self.__gsid = value        

    @property
    def cid(self) -> str:
        """Company Id Identifier"""
        return self.__cid

    @cid.setter
    def cid(self, value: str):
        self._property_changed('cid')
        self.__cid = value        

    @property
    def bbid(self) -> str:
        """Bloomberg Id Identifier"""
        return self.__bbid

    @bbid.setter
    def bbid(self, value: str):
        self._property_changed('bbid')
        self.__bbid = value        

    @property
    def bcid(self) -> str:
        """Bloomberg Composite Identifier"""
        return self.__bcid

    @bcid.setter
    def bcid(self, value: str):
        self._property_changed('bcid')
        self.__bcid = value        

    @property
    def delisted(self) -> str:
        """Whether an asset has been delisted"""
        return self.__delisted

    @delisted.setter
    def delisted(self, value: str):
        self._property_changed('delisted')
        self.__delisted = value        

    @property
    def bbid_equivalent(self) -> str:
        """Bloomberg Equivalent Identifier"""
        return self.__bbid_equivalent

    @bbid_equivalent.setter
    def bbid_equivalent(self, value: str):
        self._property_changed('bbid_equivalent')
        self.__bbid_equivalent = value        

    @property
    def cusip(self) -> str:
        """Cusip Identifier"""
        return self.__cusip

    @cusip.setter
    def cusip(self, value: str):
        self._property_changed('cusip')
        self.__cusip = value        

    @property
    def gss(self) -> str:
        """GS Symbol identifier"""
        return self.__gss

    @gss.setter
    def gss(self, value: str):
        self._property_changed('gss')
        self.__gss = value        

    @property
    def isin(self) -> str:
        """International Security Number"""
        return self.__isin

    @isin.setter
    def isin(self, value: str):
        self._property_changed('isin')
        self.__isin = value        

    @property
    def jsn(self) -> str:
        """Japan Security Number"""
        return self.__jsn

    @jsn.setter
    def jsn(self, value: str):
        self._property_changed('jsn')
        self.__jsn = value        

    @property
    def prime_id(self) -> str:
        """PrimeID Identifier"""
        return self.__prime_id

    @prime_id.setter
    def prime_id(self, value: str):
        self._property_changed('prime_id')
        self.__prime_id = value        

    @property
    def sedol(self) -> str:
        """Sedol Identifier"""
        return self.__sedol

    @sedol.setter
    def sedol(self, value: str):
        self._property_changed('sedol')
        self.__sedol = value        

    @property
    def ticker(self) -> str:
        """Ticker Identifier"""
        return self.__ticker

    @ticker.setter
    def ticker(self, value: str):
        self._property_changed('ticker')
        self.__ticker = value        

    @property
    def valoren(self) -> str:
        """Valoren Identifier"""
        return self.__valoren

    @valoren.setter
    def valoren(self, value: str):
        self._property_changed('valoren')
        self.__valoren = value        

    @property
    def wpk(self) -> str:
        """Wertpapier Kenn-Nummer"""
        return self.__wpk

    @wpk.setter
    def wpk(self, value: str):
        self._property_changed('wpk')
        self.__wpk = value        

    @property
    def gsn(self) -> str:
        """Goldman Sachs internal product number"""
        return self.__gsn

    @gsn.setter
    def gsn(self, value: str):
        self._property_changed('gsn')
        self.__gsn = value        

    @property
    def sec_name(self) -> str:
        """Internal Goldman Sachs security name"""
        return self.__sec_name

    @sec_name.setter
    def sec_name(self, value: str):
        self._property_changed('sec_name')
        self.__sec_name = value        

    @property
    def cross(self) -> str:
        """Cross identifier"""
        return self.__cross

    @cross.setter
    def cross(self, value: str):
        self._property_changed('cross')
        self.__cross = value        

    @property
    def simon_id(self) -> str:
        """SIMON product identifier"""
        return self.__simon_id

    @simon_id.setter
    def simon_id(self, value: str):
        self._property_changed('simon_id')
        self.__simon_id = value        

    @property
    def em_id(self) -> str:
        """Entity Master Identifier"""
        return self.__em_id

    @em_id.setter
    def em_id(self, value: str):
        self._property_changed('em_id')
        self.__em_id = value        

    @property
    def cm_id(self) -> str:
        """Client Master Party Id"""
        return self.__cm_id

    @cm_id.setter
    def cm_id(self, value: str):
        self._property_changed('cm_id')
        self.__cm_id = value        

    @property
    def lms_id(self) -> str:
        """Listed Market Symbol"""
        return self.__lms_id

    @lms_id.setter
    def lms_id(self, value: str):
        self._property_changed('lms_id')
        self.__lms_id = value        

    @property
    def mdapi(self) -> str:
        """MDAPI Asset"""
        return self.__mdapi

    @mdapi.setter
    def mdapi(self, value: str):
        self._property_changed('mdapi')
        self.__mdapi = value        

    @property
    def mdapi_class(self) -> str:
        """MDAPI Asset Class"""
        return self.__mdapi_class

    @mdapi_class.setter
    def mdapi_class(self, value: str):
        self._property_changed('mdapi_class')
        self.__mdapi_class = value        

    @property
    def mic(self) -> str:
        """Market Identifier Code"""
        return self.__mic

    @mic.setter
    def mic(self, value: str):
        self._property_changed('mic')
        self.__mic = value        

    @property
    def sf_id(self) -> str:
        """SalesForce ID"""
        return self.__sf_id

    @sf_id.setter
    def sf_id(self, value: str):
        self._property_changed('sf_id')
        self.__sf_id = value        

    @property
    def dollar_cross(self) -> str:
        """USD cross identifier for a particular currency"""
        return self.__dollar_cross

    @dollar_cross.setter
    def dollar_cross(self, value: str):
        self._property_changed('dollar_cross')
        self.__dollar_cross = value        

    @property
    def mq_symbol(self) -> str:
        """Marquee Symbol for generic MQ entities"""
        return self.__mq_symbol

    @mq_symbol.setter
    def mq_symbol(self, value: str):
        self._property_changed('mq_symbol')
        self.__mq_symbol = value        

    @property
    def primary_country_ric(self) -> str:
        """Reuters Primary Country Instrument Code Identifier"""
        return self.__primary_country_ric

    @primary_country_ric.setter
    def primary_country_ric(self, value: str):
        self._property_changed('primary_country_ric')
        self.__primary_country_ric = value        

    @property
    def pnode_id(self) -> str:
        """Pricing node identifier sourced from Morningstar"""
        return self.__pnode_id

    @pnode_id.setter
    def pnode_id(self, value: str):
        self._property_changed('pnode_id')
        self.__pnode_id = value        


class CSLCurrency(Base):
        
    """A currency"""

    @camel_case_translate
    def __init__(
        self,
        string_value: Union[Currency, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.string_value = string_value
        self.name = name

    @property
    def string_value(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__string_value

    @string_value.setter
    def string_value(self, value: Union[Currency, str]):
        self._property_changed('string_value')
        self.__string_value = get_enum_value(Currency, value)        


class CSLDateArray(Base):
        
    """An array of dates"""

    @camel_case_translate
    def __init__(
        self,
        date_values: Tuple[CSLDate, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.date_values = date_values
        self.name = name

    @property
    def date_values(self) -> Tuple[CSLDate, ...]:
        """A date"""
        return self.__date_values

    @date_values.setter
    def date_values(self, value: Tuple[CSLDate, ...]):
        self._property_changed('date_values')
        self.__date_values = value        


class CSLDateArrayNamedParam(Base):
        
    """A named array of dates"""

    @camel_case_translate
    def __init__(
        self,
        date_values: Tuple[CSLDate, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.date_values = date_values
        self.name = name

    @property
    def date_values(self) -> Tuple[CSLDate, ...]:
        """A date"""
        return self.__date_values

    @date_values.setter
    def date_values(self, value: Tuple[CSLDate, ...]):
        self._property_changed('date_values')
        self.__date_values = value        

    @property
    def name(self) -> str:
        """A name for the array"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        


class CSLDoubleArray(Base):
        
    """An array of doubles"""

    @camel_case_translate
    def __init__(
        self,
        double_values: Tuple[CSLDouble, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.double_values = double_values
        self.name = name

    @property
    def double_values(self) -> Tuple[CSLDouble, ...]:
        """A double"""
        return self.__double_values

    @double_values.setter
    def double_values(self, value: Tuple[CSLDouble, ...]):
        self._property_changed('double_values')
        self.__double_values = value        


class CSLFXCrossArray(Base):
        
    """An array of FX crosses"""

    @camel_case_translate
    def __init__(
        self,
        fx_cross_values: Tuple[CSLFXCross, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.fx_cross_values = fx_cross_values
        self.name = name

    @property
    def fx_cross_values(self) -> Tuple[CSLFXCross, ...]:
        """An FX cross"""
        return self.__fx_cross_values

    @fx_cross_values.setter
    def fx_cross_values(self, value: Tuple[CSLFXCross, ...]):
        self._property_changed('fx_cross_values')
        self.__fx_cross_values = value        


class CSLIndexArray(Base):
        
    """An array of indices"""

    @camel_case_translate
    def __init__(
        self,
        index_values: Tuple[CSLIndex, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.index_values = index_values
        self.name = name

    @property
    def index_values(self) -> Tuple[CSLIndex, ...]:
        """An index"""
        return self.__index_values

    @index_values.setter
    def index_values(self, value: Tuple[CSLIndex, ...]):
        self._property_changed('index_values')
        self.__index_values = value        


class CSLSimpleScheduleArray(Base):
        
    """An array of simple schedules"""

    @camel_case_translate
    def __init__(
        self,
        simple_schedule_values: Tuple[CSLSimpleSchedule, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.simple_schedule_values = simple_schedule_values
        self.name = name

    @property
    def simple_schedule_values(self) -> Tuple[CSLSimpleSchedule, ...]:
        """A fixing date, settlement date pair"""
        return self.__simple_schedule_values

    @simple_schedule_values.setter
    def simple_schedule_values(self, value: Tuple[CSLSimpleSchedule, ...]):
        self._property_changed('simple_schedule_values')
        self.__simple_schedule_values = value        


class CSLStockArray(Base):
        
    """An array of stocks"""

    @camel_case_translate
    def __init__(
        self,
        stock_values: Tuple[CSLStock, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.stock_values = stock_values
        self.name = name

    @property
    def stock_values(self) -> Tuple[CSLStock, ...]:
        """A stock"""
        return self.__stock_values

    @stock_values.setter
    def stock_values(self, value: Tuple[CSLStock, ...]):
        self._property_changed('stock_values')
        self.__stock_values = value        


class CSLStringArray(Base):
        
    """An array of strings"""

    @camel_case_translate
    def __init__(
        self,
        string_values: Tuple[CSLString, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.string_values = string_values
        self.name = name

    @property
    def string_values(self) -> Tuple[CSLString, ...]:
        """A string"""
        return self.__string_values

    @string_values.setter
    def string_values(self, value: Tuple[CSLString, ...]):
        self._property_changed('string_values')
        self.__string_values = value        


class GIRDomain(Base):
        
    @camel_case_translate
    def __init__(
        self,
        document_links: Tuple[Link, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.document_links = document_links
        self.name = name

    @property
    def document_links(self) -> Tuple[Link, ...]:
        """Documents related to this asset"""
        return self.__document_links

    @document_links.setter
    def document_links(self, value: Tuple[Link, ...]):
        self._property_changed('document_links')
        self.__document_links = value        


class ISelectNewParameter(Base):
        
    @camel_case_translate
    def __init__(
        self,
        early_unwind_after: float = None,
        early_unwind_applicable: str = None,
        expiry_date_rule: str = None,
        option_target_expiry_parameter: float = None,
        option_early_unwind_days: float = None,
        in_alpha: bool = None,
        is_fsr_target_factor: bool = None,
        fsr_max_ratio: float = None,
        fsr_min_ratio: float = None,
        module_enabled: bool = None,
        module_name: str = None,
        target_strike: float = None,
        strike_method: Union[StrikeMethodType, str] = None,
        option_expiry: Union[OptionExpiryType, str] = None,
        bloomberg_id: str = None,
        stock_id: str = None,
        new_weight: float = None,
        notional: float = None,
        option_type: Union[OptionType, str] = None,
        option_strike_type: Union[OptionStrikeType, str] = None,
        strike_relative: float = None,
        trade_type: Union[TradeType, str] = None,
        signal: float = None,
        new_signal: float = None,
        new_min_weight: float = None,
        new_max_weight: float = None,
        min_weight: float = None,
        max_weight: float = None,
        name: str = None
    ):        
        super().__init__()
        self.early_unwind_after = early_unwind_after
        self.early_unwind_applicable = early_unwind_applicable
        self.expiry_date_rule = expiry_date_rule
        self.option_target_expiry_parameter = option_target_expiry_parameter
        self.option_early_unwind_days = option_early_unwind_days
        self.in_alpha = in_alpha
        self.is_fsr_target_factor = is_fsr_target_factor
        self.fsr_max_ratio = fsr_max_ratio
        self.fsr_min_ratio = fsr_min_ratio
        self.module_enabled = module_enabled
        self.module_name = module_name
        self.target_strike = target_strike
        self.strike_method = strike_method
        self.option_expiry = option_expiry
        self.bloomberg_id = bloomberg_id
        self.stock_id = stock_id
        self.new_weight = new_weight
        self.notional = notional
        self.option_type = option_type
        self.option_strike_type = option_strike_type
        self.strike_relative = strike_relative
        self.trade_type = trade_type
        self.signal = signal
        self.new_signal = new_signal
        self.new_min_weight = new_min_weight
        self.new_max_weight = new_max_weight
        self.min_weight = min_weight
        self.max_weight = max_weight
        self.name = name

    @property
    def early_unwind_after(self) -> float:
        return self.__early_unwind_after

    @early_unwind_after.setter
    def early_unwind_after(self, value: float):
        self._property_changed('early_unwind_after')
        self.__early_unwind_after = value        

    @property
    def early_unwind_applicable(self) -> str:
        """Indicates whether the module can be unwinded early"""
        return self.__early_unwind_applicable

    @early_unwind_applicable.setter
    def early_unwind_applicable(self, value: str):
        self._property_changed('early_unwind_applicable')
        self.__early_unwind_applicable = value        

    @property
    def expiry_date_rule(self) -> str:
        """Free text description of asset. Description provided will be indexed in the
           search service for free text relevance match"""
        return self.__expiry_date_rule

    @expiry_date_rule.setter
    def expiry_date_rule(self, value: str):
        self._property_changed('expiry_date_rule')
        self.__expiry_date_rule = value        

    @property
    def option_target_expiry_parameter(self) -> float:
        return self.__option_target_expiry_parameter

    @option_target_expiry_parameter.setter
    def option_target_expiry_parameter(self, value: float):
        self._property_changed('option_target_expiry_parameter')
        self.__option_target_expiry_parameter = value        

    @property
    def option_early_unwind_days(self) -> float:
        return self.__option_early_unwind_days

    @option_early_unwind_days.setter
    def option_early_unwind_days(self, value: float):
        self._property_changed('option_early_unwind_days')
        self.__option_early_unwind_days = value        

    @property
    def in_alpha(self) -> bool:
        return self.__in_alpha

    @in_alpha.setter
    def in_alpha(self, value: bool):
        self._property_changed('in_alpha')
        self.__in_alpha = value        

    @property
    def is_fsr_target_factor(self) -> bool:
        return self.__is_fsr_target_factor

    @is_fsr_target_factor.setter
    def is_fsr_target_factor(self, value: bool):
        self._property_changed('is_fsr_target_factor')
        self.__is_fsr_target_factor = value        

    @property
    def fsr_max_ratio(self) -> float:
        return self.__fsr_max_ratio

    @fsr_max_ratio.setter
    def fsr_max_ratio(self, value: float):
        self._property_changed('fsr_max_ratio')
        self.__fsr_max_ratio = value        

    @property
    def fsr_min_ratio(self) -> float:
        return self.__fsr_min_ratio

    @fsr_min_ratio.setter
    def fsr_min_ratio(self, value: float):
        self._property_changed('fsr_min_ratio')
        self.__fsr_min_ratio = value        

    @property
    def module_enabled(self) -> bool:
        """Enable to disable the module"""
        return self.__module_enabled

    @module_enabled.setter
    def module_enabled(self, value: bool):
        self._property_changed('module_enabled')
        self.__module_enabled = value        

    @property
    def module_name(self) -> str:
        """Free text description of asset. Description provided will be indexed in the
           search service for free text relevance match"""
        return self.__module_name

    @module_name.setter
    def module_name(self, value: str):
        self._property_changed('module_name')
        self.__module_name = value        

    @property
    def target_strike(self) -> float:
        return self.__target_strike

    @target_strike.setter
    def target_strike(self, value: float):
        self._property_changed('target_strike')
        self.__target_strike = value        

    @property
    def strike_method(self) -> Union[StrikeMethodType, str]:
        return self.__strike_method

    @strike_method.setter
    def strike_method(self, value: Union[StrikeMethodType, str]):
        self._property_changed('strike_method')
        self.__strike_method = get_enum_value(StrikeMethodType, value)        

    @property
    def option_expiry(self) -> Union[OptionExpiryType, str]:
        return self.__option_expiry

    @option_expiry.setter
    def option_expiry(self, value: Union[OptionExpiryType, str]):
        self._property_changed('option_expiry')
        self.__option_expiry = get_enum_value(OptionExpiryType, value)        

    @property
    def bloomberg_id(self) -> str:
        return self.__bloomberg_id

    @bloomberg_id.setter
    def bloomberg_id(self, value: str):
        self._property_changed('bloomberg_id')
        self.__bloomberg_id = value        

    @property
    def stock_id(self) -> str:
        return self.__stock_id

    @stock_id.setter
    def stock_id(self, value: str):
        self._property_changed('stock_id')
        self.__stock_id = value        

    @property
    def new_weight(self) -> float:
        return self.__new_weight

    @new_weight.setter
    def new_weight(self, value: float):
        self._property_changed('new_weight')
        self.__new_weight = value        

    @property
    def notional(self) -> float:
        return self.__notional

    @notional.setter
    def notional(self, value: float):
        self._property_changed('notional')
        self.__notional = value        

    @property
    def option_type(self) -> Union[OptionType, str]:
        return self.__option_type

    @option_type.setter
    def option_type(self, value: Union[OptionType, str]):
        self._property_changed('option_type')
        self.__option_type = get_enum_value(OptionType, value)        

    @property
    def option_strike_type(self) -> Union[OptionStrikeType, str]:
        return self.__option_strike_type

    @option_strike_type.setter
    def option_strike_type(self, value: Union[OptionStrikeType, str]):
        self._property_changed('option_strike_type')
        self.__option_strike_type = get_enum_value(OptionStrikeType, value)        

    @property
    def strike_relative(self) -> float:
        return self.__strike_relative

    @strike_relative.setter
    def strike_relative(self, value: float):
        self._property_changed('strike_relative')
        self.__strike_relative = value        

    @property
    def trade_type(self) -> Union[TradeType, str]:
        """Direction"""
        return self.__trade_type

    @trade_type.setter
    def trade_type(self, value: Union[TradeType, str]):
        self._property_changed('trade_type')
        self.__trade_type = get_enum_value(TradeType, value)        

    @property
    def signal(self) -> float:
        return self.__signal

    @signal.setter
    def signal(self, value: float):
        self._property_changed('signal')
        self.__signal = value        

    @property
    def new_signal(self) -> float:
        return self.__new_signal

    @new_signal.setter
    def new_signal(self, value: float):
        self._property_changed('new_signal')
        self.__new_signal = value        

    @property
    def new_min_weight(self) -> float:
        return self.__new_min_weight

    @new_min_weight.setter
    def new_min_weight(self, value: float):
        self._property_changed('new_min_weight')
        self.__new_min_weight = value        

    @property
    def new_max_weight(self) -> float:
        return self.__new_max_weight

    @new_max_weight.setter
    def new_max_weight(self, value: float):
        self._property_changed('new_max_weight')
        self.__new_max_weight = value        

    @property
    def min_weight(self) -> float:
        return self.__min_weight

    @min_weight.setter
    def min_weight(self, value: float):
        self._property_changed('min_weight')
        self.__min_weight = value        

    @property
    def max_weight(self) -> float:
        return self.__max_weight

    @max_weight.setter
    def max_weight(self, value: float):
        self._property_changed('max_weight')
        self.__max_weight = value        


class MarketDataPattern(Base):
        
    """A pattern used to match market coordinates"""

    @camel_case_translate
    def __init__(
        self,
        mkt_type: str = None,
        mkt_asset: str = None,
        mkt_class: str = None,
        mkt_point: Tuple[str, ...] = None,
        mkt_quoting_style: str = None,
        is_active: bool = None,
        is_investment_grade: bool = None,
        currency: Union[Currency, str] = None,
        country_code: Union[CountryCode, str] = None,
        gics_sector: str = None,
        gics_industry_group: str = None,
        gics_industry: str = None,
        gics_sub_industry: str = None,
        name: str = None
    ):        
        super().__init__()
        self.mkt_type = mkt_type
        self.mkt_asset = mkt_asset
        self.mkt_class = mkt_class
        self.mkt_point = mkt_point
        self.mkt_quoting_style = mkt_quoting_style
        self.is_active = is_active
        self.is_investment_grade = is_investment_grade
        self.currency = currency
        self.country_code = country_code
        self.gics_sector = gics_sector
        self.gics_industry_group = gics_industry_group
        self.gics_industry = gics_industry
        self.gics_sub_industry = gics_sub_industry
        self.name = name

    @property
    def mkt_type(self) -> str:
        """The Market Data Type, e.g. IR, IR_BASIS, FX, FX_Vol"""
        return self.__mkt_type

    @mkt_type.setter
    def mkt_type(self, value: str):
        self._property_changed('mkt_type')
        self.__mkt_type = value        

    @property
    def mkt_asset(self) -> str:
        """The specific point, e.g. 3m, 10y, 11y, Dec19"""
        return self.__mkt_asset

    @mkt_asset.setter
    def mkt_asset(self, value: str):
        self._property_changed('mkt_asset')
        self.__mkt_asset = value        

    @property
    def mkt_class(self) -> str:
        """The market data pointClass, e.g. Swap, Cash."""
        return self.__mkt_class

    @mkt_class.setter
    def mkt_class(self, value: str):
        self._property_changed('mkt_class')
        self.__mkt_class = value        

    @property
    def mkt_point(self) -> Tuple[str, ...]:
        """The specific point, e.g. 3m, 10y, 11y, Dec19"""
        return self.__mkt_point

    @mkt_point.setter
    def mkt_point(self, value: Tuple[str, ...]):
        self._property_changed('mkt_point')
        self.__mkt_point = value        

    @property
    def mkt_quoting_style(self) -> str:
        return self.__mkt_quoting_style

    @mkt_quoting_style.setter
    def mkt_quoting_style(self, value: str):
        self._property_changed('mkt_quoting_style')
        self.__mkt_quoting_style = value        

    @property
    def is_active(self) -> bool:
        """Is the asset active"""
        return self.__is_active

    @is_active.setter
    def is_active(self, value: bool):
        self._property_changed('is_active')
        self.__is_active = value        

    @property
    def is_investment_grade(self) -> bool:
        """Is the asset investment grade"""
        return self.__is_investment_grade

    @is_investment_grade.setter
    def is_investment_grade(self, value: bool):
        self._property_changed('is_investment_grade')
        self.__is_investment_grade = value        

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self._property_changed('currency')
        self.__currency = get_enum_value(Currency, value)        

    @property
    def country_code(self) -> Union[CountryCode, str]:
        """ISO Country code"""
        return self.__country_code

    @country_code.setter
    def country_code(self, value: Union[CountryCode, str]):
        self._property_changed('country_code')
        self.__country_code = get_enum_value(CountryCode, value)        

    @property
    def gics_sector(self) -> str:
        """GICS Sector classification (level 1)"""
        return self.__gics_sector

    @gics_sector.setter
    def gics_sector(self, value: str):
        self._property_changed('gics_sector')
        self.__gics_sector = value        

    @property
    def gics_industry_group(self) -> str:
        """GICS Industry Group classification (level 2)"""
        return self.__gics_industry_group

    @gics_industry_group.setter
    def gics_industry_group(self, value: str):
        self._property_changed('gics_industry_group')
        self.__gics_industry_group = value        

    @property
    def gics_industry(self) -> str:
        """GICS Industry classification (level 3)"""
        return self.__gics_industry

    @gics_industry.setter
    def gics_industry(self, value: str):
        self._property_changed('gics_industry')
        self.__gics_industry = value        

    @property
    def gics_sub_industry(self) -> str:
        """GICS Sub Industry classification (level 4)"""
        return self.__gics_sub_industry

    @gics_sub_industry.setter
    def gics_sub_industry(self, value: str):
        self._property_changed('gics_sub_industry')
        self.__gics_sub_industry = value        


class MarketDataShock(Base):
        
    """A shock to apply to market coordinate values"""

    @camel_case_translate
    def __init__(
        self,
        shock_type: Union[MarketDataShockType, str],
        value: float,
        precision: float = None,
        cap: float = None,
        floor: float = None,
        coordinate_cap: float = None,
        coordinate_floor: float = None,
        name: str = None
    ):        
        super().__init__()
        self.shock_type = shock_type
        self.value = value
        self.precision = precision
        self.cap = cap
        self.floor = floor
        self.coordinate_cap = coordinate_cap
        self.coordinate_floor = coordinate_floor
        self.name = name

    @property
    def shock_type(self) -> Union[MarketDataShockType, str]:
        """Market data shock type"""
        return self.__shock_type

    @shock_type.setter
    def shock_type(self, value: Union[MarketDataShockType, str]):
        self._property_changed('shock_type')
        self.__shock_type = get_enum_value(MarketDataShockType, value)        

    @property
    def value(self) -> float:
        """The amount by which to shock matching coordinates"""
        return self.__value

    @value.setter
    def value(self, value: float):
        self._property_changed('value')
        self.__value = value        

    @property
    def precision(self) -> float:
        """The precision to which the shock will be rounded"""
        return self.__precision

    @precision.setter
    def precision(self, value: float):
        self._property_changed('precision')
        self.__precision = value        

    @property
    def cap(self) -> float:
        """Upper bound on the shocked value"""
        return self.__cap

    @cap.setter
    def cap(self, value: float):
        self._property_changed('cap')
        self.__cap = value        

    @property
    def floor(self) -> float:
        """Lower bound on the shocked value"""
        return self.__floor

    @floor.setter
    def floor(self, value: float):
        self._property_changed('floor')
        self.__floor = value        

    @property
    def coordinate_cap(self) -> float:
        """Upper bound on the pre-shocked value of matching coordinates"""
        return self.__coordinate_cap

    @coordinate_cap.setter
    def coordinate_cap(self, value: float):
        self._property_changed('coordinate_cap')
        self.__coordinate_cap = value        

    @property
    def coordinate_floor(self) -> float:
        """Lower bound on the pre-shocked value of matching coordinates"""
        return self.__coordinate_floor

    @coordinate_floor.setter
    def coordinate_floor(self, value: float):
        self._property_changed('coordinate_floor')
        self.__coordinate_floor = value        


class RiskMeasure(Base):
        
    """The measure to perform risk on. Each risk measure consists of an asset class, a
       measure type, and a unit."""

    @camel_case_translate
    def __init__(
        self,
        asset_class: Union[AssetClass, str] = None,
        measure_type: Union[RiskMeasureType, str] = None,
        unit: Union[RiskMeasureUnit, str] = None,
        value: Union[float, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.asset_class = asset_class
        self.measure_type = measure_type
        self.unit = unit
        self.value = value
        self.name = name

    @property
    def asset_class(self) -> Union[AssetClass, str]:
        """Asset classification of security. Assets are classified into broad groups which
           exhibit similar characteristics and behave in a consistent way under
           different market conditions"""
        return self.__asset_class

    @asset_class.setter
    def asset_class(self, value: Union[AssetClass, str]):
        self._property_changed('asset_class')
        self.__asset_class = get_enum_value(AssetClass, value)        

    @property
    def measure_type(self) -> Union[RiskMeasureType, str]:
        """The type of measure to perform risk on. e.g. Greeks"""
        return self.__measure_type

    @measure_type.setter
    def measure_type(self, value: Union[RiskMeasureType, str]):
        self._property_changed('measure_type')
        self.__measure_type = get_enum_value(RiskMeasureType, value)        

    @property
    def unit(self) -> Union[RiskMeasureUnit, str]:
        """The unit of change of underlying in the risk computation."""
        return self.__unit

    @unit.setter
    def unit(self, value: Union[RiskMeasureUnit, str]):
        self._property_changed('unit')
        self.__unit = get_enum_value(RiskMeasureUnit, value)        

    @property
    def value(self) -> Union[float, str]:
        """Value of this measure"""
        return self.__value

    @value.setter
    def value(self, value: Union[float, str]):
        self._property_changed('value')
        self.__value = value        


class CSLCurrencyArray(Base):
        
    """An array of currencies"""

    @camel_case_translate
    def __init__(
        self,
        currency_values: Tuple[CSLCurrency, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.currency_values = currency_values
        self.name = name

    @property
    def currency_values(self) -> Tuple[CSLCurrency, ...]:
        """A currency"""
        return self.__currency_values

    @currency_values.setter
    def currency_values(self, value: Tuple[CSLCurrency, ...]):
        self._property_changed('currency_values')
        self.__currency_values = value        


class CSLSchedule(Base):
        
    """A schedule"""

    @camel_case_translate
    def __init__(
        self,
        first_date: datetime.date = None,
        last_date: datetime.date = None,
        calendar_name: str = None,
        period: str = None,
        delay: str = None,
        business_day_convention: str = None,
        day_count_convention: str = None,
        days_per_term: str = None,
        delay_business_day_convention: str = None,
        delay_calendar_name: str = None,
        has_reset_date: bool = None,
        term_formula: str = None,
        extra_dates: Tuple[CSLDateArrayNamedParam, ...] = None,
        extra_dates_by_offset: Tuple[CSLSymCaseNamedParam, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.first_date = first_date
        self.last_date = last_date
        self.calendar_name = calendar_name
        self.period = period
        self.delay = delay
        self.business_day_convention = business_day_convention
        self.day_count_convention = day_count_convention
        self.days_per_term = days_per_term
        self.delay_business_day_convention = delay_business_day_convention
        self.delay_calendar_name = delay_calendar_name
        self.has_reset_date = has_reset_date
        self.term_formula = term_formula
        self.extra_dates = extra_dates
        self.extra_dates_by_offset = extra_dates_by_offset
        self.name = name

    @property
    def first_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__first_date

    @first_date.setter
    def first_date(self, value: datetime.date):
        self._property_changed('first_date')
        self.__first_date = value        

    @property
    def last_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__last_date

    @last_date.setter
    def last_date(self, value: datetime.date):
        self._property_changed('last_date')
        self.__last_date = value        

    @property
    def calendar_name(self) -> str:
        """The name of the holiday calendar"""
        return self.__calendar_name

    @calendar_name.setter
    def calendar_name(self, value: str):
        self._property_changed('calendar_name')
        self.__calendar_name = value        

    @property
    def period(self) -> str:
        """Tenor"""
        return self.__period

    @period.setter
    def period(self, value: str):
        self._property_changed('period')
        self.__period = value        

    @property
    def delay(self) -> str:
        """The delay"""
        return self.__delay

    @delay.setter
    def delay(self, value: str):
        self._property_changed('delay')
        self.__delay = value        

    @property
    def business_day_convention(self) -> str:
        return self.__business_day_convention

    @business_day_convention.setter
    def business_day_convention(self, value: str):
        self._property_changed('business_day_convention')
        self.__business_day_convention = value        

    @property
    def day_count_convention(self) -> str:
        return self.__day_count_convention

    @day_count_convention.setter
    def day_count_convention(self, value: str):
        self._property_changed('day_count_convention')
        self.__day_count_convention = value        

    @property
    def days_per_term(self) -> str:
        return self.__days_per_term

    @days_per_term.setter
    def days_per_term(self, value: str):
        self._property_changed('days_per_term')
        self.__days_per_term = value        

    @property
    def delay_business_day_convention(self) -> str:
        return self.__delay_business_day_convention

    @delay_business_day_convention.setter
    def delay_business_day_convention(self, value: str):
        self._property_changed('delay_business_day_convention')
        self.__delay_business_day_convention = value        

    @property
    def delay_calendar_name(self) -> str:
        """The name of the holiday calendar"""
        return self.__delay_calendar_name

    @delay_calendar_name.setter
    def delay_calendar_name(self, value: str):
        self._property_changed('delay_calendar_name')
        self.__delay_calendar_name = value        

    @property
    def has_reset_date(self) -> bool:
        return self.__has_reset_date

    @has_reset_date.setter
    def has_reset_date(self, value: bool):
        self._property_changed('has_reset_date')
        self.__has_reset_date = value        

    @property
    def term_formula(self) -> str:
        return self.__term_formula

    @term_formula.setter
    def term_formula(self, value: str):
        self._property_changed('term_formula')
        self.__term_formula = value        

    @property
    def extra_dates(self) -> Tuple[CSLDateArrayNamedParam, ...]:
        """A named array of dates"""
        return self.__extra_dates

    @extra_dates.setter
    def extra_dates(self, value: Tuple[CSLDateArrayNamedParam, ...]):
        self._property_changed('extra_dates')
        self.__extra_dates = value        

    @property
    def extra_dates_by_offset(self) -> Tuple[CSLSymCaseNamedParam, ...]:
        """A named case-sensitive string."""
        return self.__extra_dates_by_offset

    @extra_dates_by_offset.setter
    def extra_dates_by_offset(self, value: Tuple[CSLSymCaseNamedParam, ...]):
        self._property_changed('extra_dates_by_offset')
        self.__extra_dates_by_offset = value        


class CurveScenario(Scenario):
        
    """A scenario to manipulate curve shape"""

    @camel_case_translate
    def __init__(
        self,
        market_data_pattern: MarketDataPattern = None,
        annualised_parallel_shift: float = None,
        annualised_slope_shift: float = None,
        pivot_point: float = None,
        cutoff: float = None,
        name: str = None
    ):        
        super().__init__()
        self.market_data_pattern = market_data_pattern
        self.annualised_parallel_shift = annualised_parallel_shift
        self.annualised_slope_shift = annualised_slope_shift
        self.pivot_point = pivot_point
        self.cutoff = cutoff
        self.name = name

    @property
    def scenario_type(self) -> str:
        """CurveScenario"""
        return 'CurveScenario'        

    @property
    def market_data_pattern(self) -> MarketDataPattern:
        """Market pattern for matching curve assets"""
        return self.__market_data_pattern

    @market_data_pattern.setter
    def market_data_pattern(self, value: MarketDataPattern):
        self._property_changed('market_data_pattern')
        self.__market_data_pattern = value        

    @property
    def annualised_parallel_shift(self) -> float:
        """Size of the parallel shift (in bps/year)"""
        return self.__annualised_parallel_shift

    @annualised_parallel_shift.setter
    def annualised_parallel_shift(self, value: float):
        self._property_changed('annualised_parallel_shift')
        self.__annualised_parallel_shift = value        

    @property
    def annualised_slope_shift(self) -> float:
        """Size of the slope shift (in bps/year)"""
        return self.__annualised_slope_shift

    @annualised_slope_shift.setter
    def annualised_slope_shift(self, value: float):
        self._property_changed('annualised_slope_shift')
        self.__annualised_slope_shift = value        

    @property
    def pivot_point(self) -> float:
        """The pivot point (in years)"""
        return self.__pivot_point

    @pivot_point.setter
    def pivot_point(self, value: float):
        self._property_changed('pivot_point')
        self.__pivot_point = value        

    @property
    def cutoff(self) -> float:
        """The cutoff point (in years)"""
        return self.__cutoff

    @cutoff.setter
    def cutoff(self, value: float):
        self._property_changed('cutoff')
        self.__cutoff = value        


class DataSetFieldMap(Base):
        
    """The mapping between data set field and risk measure type"""

    @camel_case_translate
    def __init__(
        self,
        data_set_id: str,
        field: str,
        results_field: str,
        risk_measure: RiskMeasure,
        name: str = None
    ):        
        super().__init__()
        self.data_set_id = data_set_id
        self.field = field
        self.results_field = results_field
        self.risk_measure = risk_measure
        self.name = name

    @property
    def data_set_id(self) -> str:
        """Unique id of dataset."""
        return self.__data_set_id

    @data_set_id.setter
    def data_set_id(self, value: str):
        self._property_changed('data_set_id')
        self.__data_set_id = value        

    @property
    def field(self) -> str:
        """The field for data set, e.g. rate"""
        return self.__field

    @field.setter
    def field(self, value: str):
        self._property_changed('field')
        self.__field = value        

    @property
    def results_field(self) -> str:
        """The source field in the results, e.g. value or fixedRate"""
        return self.__results_field

    @results_field.setter
    def results_field(self, value: str):
        self._property_changed('results_field')
        self.__results_field = value        

    @property
    def risk_measure(self) -> RiskMeasure:
        """The measure to perform risk on. Each risk measure consists of an asset class, a
           measure type, and a unit."""
        return self.__risk_measure

    @risk_measure.setter
    def risk_measure(self, value: RiskMeasure):
        self._property_changed('risk_measure')
        self.__risk_measure = value        


class FieldFilterMap(Base):
        
    @camel_case_translate
    def __init__(
        self,
        **kwargs
    ):        
        super().__init__()
        self.collateral_value_variance = kwargs.get('collateral_value_variance')
        self.year = kwargs.get('year')
        self.investment_rate = kwargs.get('investment_rate')
        self.forecast_period = kwargs.get('forecast_period')
        self.mdapi_class = kwargs.get('mdapi_class')
        self.data_set_ids = kwargs.get('data_set_ids')
        self.bid_unadjusted = kwargs.get('bid_unadjusted')
        self.economic_terms_hash = kwargs.get('economic_terms_hash')
        self.client_type = kwargs.get('client_type')
        self.available_inventory = kwargs.get('available_inventory')
        self.est1_day_complete_pct = kwargs.get('est1_day_complete_pct')
        self.created_by_id = kwargs.get('created_by_id')
        self.vehicle_type = kwargs.get('vehicle_type')
        self.daily_risk = kwargs.get('daily_risk')
        self.energy = kwargs.get('energy')
        self.market_data_type = kwargs.get('market_data_type')
        self.real_short_rates_contribution = kwargs.get('real_short_rates_contribution')
        self.sentiment_score = kwargs.get('sentiment_score')
        self.leg_one_payment_type = kwargs.get('leg_one_payment_type')
        self.provide_tape_c = kwargs.get('provide_tape_c')
        self.value_previous = kwargs.get('value_previous')
        self.delivery_point_leg2 = kwargs.get('delivery_point_leg2')
        self.avg_trade_rate = kwargs.get('avg_trade_rate')
        self.short_level = kwargs.get('short_level')
        self.version = kwargs.get('version')
        self.policy_rate_expectation = kwargs.get('policy_rate_expectation')
        self.correlation = kwargs.get('correlation')
        self.exposure = kwargs.get('exposure')
        self.market_data_asset = kwargs.get('market_data_asset')
        self.earnings_per_share_positive = kwargs.get('earnings_per_share_positive')
        self.unadjusted_high = kwargs.get('unadjusted_high')
        self.source_importance = kwargs.get('source_importance')
        self.eid = kwargs.get('eid')
        self.relative_return_qtd = kwargs.get('relative_return_qtd')
        self.display_name = kwargs.get('display_name')
        self.minutes_to_trade100_pct = kwargs.get('minutes_to_trade100_pct')
        self.mkt_quoting_style = kwargs.get('mkt_quoting_style')
        self.expiration_tenor = kwargs.get('expiration_tenor')
        self.market_model_id = kwargs.get('market_model_id')
        self.realized_correlation = kwargs.get('realized_correlation')
        self.collateral_value_actual = kwargs.get('collateral_value_actual')
        self.upfront_payment = kwargs.get('upfront_payment')
        self.atm_fwd_rate = kwargs.get('atm_fwd_rate')
        self.provide_tape_a = kwargs.get('provide_tape_a')
        self.provide_tape_b = kwargs.get('provide_tape_b')
        self.tcm_cost_participation_rate75_pct = kwargs.get('tcm_cost_participation_rate75_pct')
        self.close = kwargs.get('close')
        self.a = kwargs.get('a')
        self.b = kwargs.get('b')
        self.c = kwargs.get('c')
        self.equity_vega = kwargs.get('equity_vega')
        self.leg_one_spread = kwargs.get('leg_one_spread')
        self.lender_payment = kwargs.get('lender_payment')
        self.five_day_move = kwargs.get('five_day_move')
        self.geography_name = kwargs.get('geography_name')
        self.borrower = kwargs.get('borrower')
        self.value_format = kwargs.get('value_format')
        self.performance_contribution = kwargs.get('performance_contribution')
        self.target_notional = kwargs.get('target_notional')
        self.fill_leg_id = kwargs.get('fill_leg_id')
        self.rationale = kwargs.get('rationale')
        self.mkt_class = kwargs.get('mkt_class')
        self.last_updated_since = kwargs.get('last_updated_since')
        self.equities_contribution = kwargs.get('equities_contribution')
        self.simon_id = kwargs.get('simon_id')
        self.congestion = kwargs.get('congestion')
        self.event_category = kwargs.get('event_category')
        self.short_rates_contribution = kwargs.get('short_rates_contribution')
        self.implied_normal_volatility = kwargs.get('implied_normal_volatility')
        self.unadjusted_open = kwargs.get('unadjusted_open')
        self.criticality = kwargs.get('criticality')
        self.mtm_price = kwargs.get('mtm_price')
        self.bid_ask_spread = kwargs.get('bid_ask_spread')
        self.leg_one_averaging_method = kwargs.get('leg_one_averaging_method')
        self.option_type = kwargs.get('option_type')
        self.portfolio_assets = kwargs.get('portfolio_assets')
        self.tcm_cost_horizon3_hour = kwargs.get('tcm_cost_horizon3_hour')
        self.number_covered = kwargs.get('number_covered')
        self.credit_limit = kwargs.get('credit_limit')
        self.number_of_positions = kwargs.get('number_of_positions')
        self.effective_tenor = kwargs.get('effective_tenor')
        self.open_unadjusted = kwargs.get('open_unadjusted')
        self.ask_price = kwargs.get('ask_price')
        self.event_id = kwargs.get('event_id')
        self.sectors = kwargs.get('sectors')
        self.std30_days_subsidized_yield = kwargs.get('std30_days_subsidized_yield')
        self.annualized_tracking_error = kwargs.get('annualized_tracking_error')
        self.additional_price_notation_type = kwargs.get('additional_price_notation_type')
        self.vol_swap = kwargs.get('vol_swap')
        self.real_fci = kwargs.get('real_fci')
        self.annualized_risk = kwargs.get('annualized_risk')
        self.block_trades_and_large_notional_off_facility_swaps = kwargs.get(
            'block_trades_and_large_notional_off_facility_swaps')
        self.leg_one_fixed_payment_currency = kwargs.get('leg_one_fixed_payment_currency')
        self.gross_exposure = kwargs.get('gross_exposure')
        self.payment_frequency_leg1 = kwargs.get('payment_frequency_leg1')
        self.payment_frequency_leg2 = kwargs.get('payment_frequency_leg2')
        self.volume_composite = kwargs.get('volume_composite')
        self.volume = kwargs.get('volume')
        self.adv = kwargs.get('adv')
        self.external = kwargs.get('external')
        self.short_conviction_medium = kwargs.get('short_conviction_medium')
        self.exchange = kwargs.get('exchange')
        self.trade_price = kwargs.get('trade_price')
        self.cleared = kwargs.get('cleared')
        self.es_policy_score = kwargs.get('es_policy_score')
        self.prime_id_numeric = kwargs.get('prime_id_numeric')
        self.cid = kwargs.get('cid')
        self.leg_one_index = kwargs.get('leg_one_index')
        self.on_loan_percentage = kwargs.get('on_loan_percentage')
        self.bid_high = kwargs.get('bid_high')
        self.fair_variance = kwargs.get('fair_variance')
        self.hit_rate_wtd = kwargs.get('hit_rate_wtd')
        self.bos_in_bps_description = kwargs.get('bos_in_bps_description')
        self.low_price = kwargs.get('low_price')
        self.realized_volatility = kwargs.get('realized_volatility')
        self.adv22_day_pct = kwargs.get('adv22_day_pct')
        self.clone_parent_id = kwargs.get('clone_parent_id')
        self.price_range_in_ticks_label = kwargs.get('price_range_in_ticks_label')
        self.ticker = kwargs.get('ticker')
        self.tcm_cost_horizon1_day = kwargs.get('tcm_cost_horizon1_day')
        self.approval = kwargs.get('approval')
        self.file_location = kwargs.get('file_location')
        self.sts_rates_country = kwargs.get('sts_rates_country')
        self.leg_two_payment_type = kwargs.get('leg_two_payment_type')
        self.horizon = kwargs.get('horizon')
        self.day_count_convention_leg1 = kwargs.get('day_count_convention_leg1')
        self.source_value_forecast = kwargs.get('source_value_forecast')
        self.short_conviction_large = kwargs.get('short_conviction_large')
        self.day_count_convention_leg2 = kwargs.get('day_count_convention_leg2')
        self.counter_party_status = kwargs.get('counter_party_status')
        self.composite22_day_adv = kwargs.get('composite22_day_adv')
        self.dollar_excess_return = kwargs.get('dollar_excess_return')
        self.gsn = kwargs.get('gsn')
        self.gss = kwargs.get('gss')
        self.percent_of_mediandv1m = kwargs.get('percent_of_mediandv1m')
        self.lendables = kwargs.get('lendables')
        self.loan_spread_required = kwargs.get('loan_spread_required')
        self.asset_class = kwargs.get('asset_class')
        self.sovereign_spread_contribution = kwargs.get('sovereign_spread_contribution')
        self.bos_in_ticks_label = kwargs.get('bos_in_ticks_label')
        self.ric = kwargs.get('ric')
        self.position_source_id = kwargs.get('position_source_id')
        self.rate_type = kwargs.get('rate_type')
        self.gs_sustain_region = kwargs.get('gs_sustain_region')
        self.deployment_id = kwargs.get('deployment_id')
        self.loan_status = kwargs.get('loan_status')
        self.short_weight = kwargs.get('short_weight')
        self.geography_id = kwargs.get('geography_id')
        self.loan_rebate = kwargs.get('loan_rebate')
        self.period = kwargs.get('period')
        self.index_create_source = kwargs.get('index_create_source')
        self.fiscal_quarter = kwargs.get('fiscal_quarter')
        self.version_string = kwargs.get('version_string')
        self.real_twi_contribution = kwargs.get('real_twi_contribution')
        self.market_impact = kwargs.get('market_impact')
        self.event_type = kwargs.get('event_type')
        self.mkt_asset = kwargs.get('mkt_asset')
        self.asset_count_long = kwargs.get('asset_count_long')
        self.spot = kwargs.get('spot')
        self.last_updated_message = kwargs.get('last_updated_message')
        self.underlying_asset_leg2 = kwargs.get('underlying_asset_leg2')
        self.loan_value = kwargs.get('loan_value')
        self.underlying_asset_leg1 = kwargs.get('underlying_asset_leg1')
        self.swap_spread = kwargs.get('swap_spread')
        self.trading_restriction = kwargs.get('trading_restriction')
        self.asset_parameters_pay_or_receive = kwargs.get('asset_parameters_pay_or_receive')
        self.price_spot_entry_unit = kwargs.get('price_spot_entry_unit')
        self.total_return_price = kwargs.get('total_return_price')
        self.weighted_percent_in_model = kwargs.get('weighted_percent_in_model')
        self.city = kwargs.get('city')
        self.election_period = kwargs.get('election_period')
        self.funding_ask_price = kwargs.get('funding_ask_price')
        self.historical_beta = kwargs.get('historical_beta')
        self.dissemination_id = kwargs.get('dissemination_id')
        self.bond_risk_premium_index = kwargs.get('bond_risk_premium_index')
        self.leg_two_fixed_payment = kwargs.get('leg_two_fixed_payment')
        self.commodity_forecast = kwargs.get('commodity_forecast')
        self.hit_rate_ytd = kwargs.get('hit_rate_ytd')
        self.valid = kwargs.get('valid')
        self.sts_commodity = kwargs.get('sts_commodity')
        self.indication_of_end_user_exception = kwargs.get('indication_of_end_user_exception')
        self.es_score = kwargs.get('es_score')
        self.price_range_in_ticks = kwargs.get('price_range_in_ticks')
        self.expense_ratio_gross_bps = kwargs.get('expense_ratio_gross_bps')
        self.pct_change = kwargs.get('pct_change')
        self.number_of_rolls = kwargs.get('number_of_rolls')
        self.agent_lender_fee = kwargs.get('agent_lender_fee')
        self.bbid = kwargs.get('bbid')
        self.option_strike_price = kwargs.get('option_strike_price')
        self.price_type_leg3 = kwargs.get('price_type_leg3')
        self.arrival_mid_normalized = kwargs.get('arrival_mid_normalized')
        self.underlying_asset2 = kwargs.get('underlying_asset2')
        self.underlying_asset1 = kwargs.get('underlying_asset1')
        self.rounded_notional_amount_leg1 = kwargs.get('rounded_notional_amount_leg1')
        self.rounded_notional_amount_leg2 = kwargs.get('rounded_notional_amount_leg2')
        self.capped = kwargs.get('capped')
        self.rating = kwargs.get('rating')
        self.payment_type_leg1 = kwargs.get('payment_type_leg1')
        self.option_currency = kwargs.get('option_currency')
        self.price_leg3 = kwargs.get('price_leg3')
        self.price_leg2 = kwargs.get('price_leg2')
        self.volatility = kwargs.get('volatility')
        self.price_leg1 = kwargs.get('price_leg1')
        self.price_type_leg2 = kwargs.get('price_type_leg2')
        self.legal_entity = kwargs.get('legal_entity')
        self.performance_fee = kwargs.get('performance_fee')
        self.price_type_leg1 = kwargs.get('price_type_leg1')
        self.payment_type_leg2 = kwargs.get('payment_type_leg2')
        self.type_leg1 = kwargs.get('type_leg1')
        self.underlying_asset_ids = kwargs.get('underlying_asset_ids')
        self.type_leg2 = kwargs.get('type_leg2')
        self.queue_in_lots_label = kwargs.get('queue_in_lots_label')
        self.adv10_day_pct = kwargs.get('adv10_day_pct')
        self.long_conviction_medium = kwargs.get('long_conviction_medium')
        self.annual_risk = kwargs.get('annual_risk')
        self.eti = kwargs.get('eti')
        self.daily_tracking_error = kwargs.get('daily_tracking_error')
        self.leg_two_index = kwargs.get('leg_two_index')
        self.market_buffer = kwargs.get('market_buffer')
        self.market_cap = kwargs.get('market_cap')
        self.oe_id = kwargs.get('oe_id')
        self.cluster_region = kwargs.get('cluster_region')
        self.bbid_equivalent = kwargs.get('bbid_equivalent')
        self.valoren = kwargs.get('valoren')
        self.basis = kwargs.get('basis')
        self.investment_rate_trend = kwargs.get('investment_rate_trend')
        self.ext_mkt_class = kwargs.get('ext_mkt_class')
        self.price_currency = kwargs.get('price_currency')
        self.hedge_id = kwargs.get('hedge_id')
        self.tcm_cost_horizon8_day = kwargs.get('tcm_cost_horizon8_day')
        self.residual_variance = kwargs.get('residual_variance')
        self.supra_strategy = kwargs.get('supra_strategy')
        self.restrict_internal_derived_data = kwargs.get('restrict_internal_derived_data')
        self.day_count_convention = kwargs.get('day_count_convention')
        self.rounded_notional_amount1 = kwargs.get('rounded_notional_amount1')
        self.adv5_day_pct = kwargs.get('adv5_day_pct')
        self.rounded_notional_amount2 = kwargs.get('rounded_notional_amount2')
        self.factor_source = kwargs.get('factor_source')
        self.lending_sec_type = kwargs.get('lending_sec_type')
        self.leverage = kwargs.get('leverage')
        self.option_family = kwargs.get('option_family')
        self.price_spot_stop_loss_value = kwargs.get('price_spot_stop_loss_value')
        self.fwd_points = kwargs.get('fwd_points')
        self.kpi_id = kwargs.get('kpi_id')
        self.relative_return_wtd = kwargs.get('relative_return_wtd')
        self.borrow_cost = kwargs.get('borrow_cost')
        self.asset_classifications_risk_country_name = kwargs.get('asset_classifications_risk_country_name')
        self.risk_model = kwargs.get('risk_model')
        self.average_implied_volatility = kwargs.get('average_implied_volatility')
        self.fair_value = kwargs.get('fair_value')
        self.adjusted_high_price = kwargs.get('adjusted_high_price')
        self.local_ccy_rate = kwargs.get('local_ccy_rate')
        self.ext_mkt_point1 = kwargs.get('ext_mkt_point1')
        self.direction = kwargs.get('direction')
        self.ext_mkt_point2 = kwargs.get('ext_mkt_point2')
        self.sub_region_code = kwargs.get('sub_region_code')
        self.value_forecast = kwargs.get('value_forecast')
        self.execution_venue = kwargs.get('execution_venue')
        self.position_source_type = kwargs.get('position_source_type')
        self.approve_rebalance = kwargs.get('approve_rebalance')
        self.adjusted_close_price = kwargs.get('adjusted_close_price')
        self.lms_id = kwargs.get('lms_id')
        self.rebate_rate = kwargs.get('rebate_rate')
        self.participation_rate = kwargs.get('participation_rate')
        self.obfr = kwargs.get('obfr')
        self.option_lock_period = kwargs.get('option_lock_period')
        self.strike_relative = kwargs.get('strike_relative')
        self.es_momentum_percentile = kwargs.get('es_momentum_percentile')
        self.price_notation = kwargs.get('price_notation')
        self.strategy = kwargs.get('strategy')
        self.position_type = kwargs.get('position_type')
        self.lender_income = kwargs.get('lender_income')
        self.sub_asset_class = kwargs.get('sub_asset_class')
        self.provide_mpl_tape_b = kwargs.get('provide_mpl_tape_b')
        self.short_interest = kwargs.get('short_interest')
        self.reference_period = kwargs.get('reference_period')
        self.provide_mpl_tape_c = kwargs.get('provide_mpl_tape_c')
        self.adjusted_volume = kwargs.get('adjusted_volume')
        self.provide_mpl_tape_a = kwargs.get('provide_mpl_tape_a')
        self.pb_client_id = kwargs.get('pb_client_id')
        self.owner_id = kwargs.get('owner_id')
        self.sec_db = kwargs.get('sec_db')
        self.composite10_day_adv = kwargs.get('composite10_day_adv')
        self.bpe_quality_stars = kwargs.get('bpe_quality_stars')
        self.idea_activity_type = kwargs.get('idea_activity_type')
        self.idea_source = kwargs.get('idea_source')
        self.unadjusted_ask = kwargs.get('unadjusted_ask')
        self.trading_pnl = kwargs.get('trading_pnl')
        self.collateral_value_required = kwargs.get('collateral_value_required')
        self.given_plus_paid = kwargs.get('given_plus_paid')
        self.short_conviction_small = kwargs.get('short_conviction_small')
        self.price_to_earnings_positive = kwargs.get('price_to_earnings_positive')
        self.forecast = kwargs.get('forecast')
        self.pnl = kwargs.get('pnl')
        self.upfront_payment_currency = kwargs.get('upfront_payment_currency')
        self.date_index = kwargs.get('date_index')
        self.tcm_cost_horizon4_day = kwargs.get('tcm_cost_horizon4_day')
        self.asset_classifications_is_primary = kwargs.get('asset_classifications_is_primary')
        self.styles = kwargs.get('styles')
        self.short_name = kwargs.get('short_name')
        self.dwi_contribution = kwargs.get('dwi_contribution')
        self.reset_frequency1 = kwargs.get('reset_frequency1')
        self.asset2_id = kwargs.get('asset2_id')
        self.reset_frequency2 = kwargs.get('reset_frequency2')
        self.average_fill_price = kwargs.get('average_fill_price')
        self.price_notation_type2 = kwargs.get('price_notation_type2')
        self.price_notation_type3 = kwargs.get('price_notation_type3')
        self.bid_gspread = kwargs.get('bid_gspread')
        self.open_price = kwargs.get('open_price')
        self.depth_spread_score = kwargs.get('depth_spread_score')
        self.sub_account = kwargs.get('sub_account')
        self.notional_currency_leg1 = kwargs.get('notional_currency_leg1')
        self.notional_currency_leg2 = kwargs.get('notional_currency_leg2')
        self.fair_volatility = kwargs.get('fair_volatility')
        self.dollar_cross = kwargs.get('dollar_cross')
        self.portfolio_type = kwargs.get('portfolio_type')
        self.vendor = kwargs.get('vendor')
        self.currency = kwargs.get('currency')
        self.cluster_class = kwargs.get('cluster_class')
        self.queueing_time = kwargs.get('queueing_time')
        self.ann_return5_year = kwargs.get('ann_return5_year')
        self.bid_size = kwargs.get('bid_size')
        self.arrival_mid = kwargs.get('arrival_mid')
        self.business_sponsor = kwargs.get('business_sponsor')
        self.asset_parameters_exchange_currency = kwargs.get('asset_parameters_exchange_currency')
        self.unexplained = kwargs.get('unexplained')
        self.candidate_name = kwargs.get('candidate_name')
        self.metric = kwargs.get('metric')
        self.ask = kwargs.get('ask')
        self.implied_lognormal_volatility = kwargs.get('implied_lognormal_volatility')
        self.close_price = kwargs.get('close_price')
        self.absolute_strike = kwargs.get('absolute_strike')
        self.source = kwargs.get('source')
        self.asset_classifications_country_code = kwargs.get('asset_classifications_country_code')
        self.expense_ratio_net_bps = kwargs.get('expense_ratio_net_bps')
        self.data_set_sub_category = kwargs.get('data_set_sub_category')
        self.day_count_convention2 = kwargs.get('day_count_convention2')
        self.quantity_bucket = kwargs.get('quantity_bucket')
        self.factor_two = kwargs.get('factor_two')
        self.oe_name = kwargs.get('oe_name')
        self.given = kwargs.get('given')
        self.delisting_date = kwargs.get('delisting_date')
        self.price_spot_target_value = kwargs.get('price_spot_target_value')
        self.weight = kwargs.get('weight')
        self.business_scope = kwargs.get('business_scope')
        self.market_data_point = kwargs.get('market_data_point')
        self.absolute_weight = kwargs.get('absolute_weight')
        self.measure = kwargs.get('measure')
        self.hedge_annualized_volatility = kwargs.get('hedge_annualized_volatility')
        self.benchmark_currency = kwargs.get('benchmark_currency')
        self.futures_contract = kwargs.get('futures_contract')
        self.name = kwargs.get('name')
        self.aum = kwargs.get('aum')
        self.folder_name = kwargs.get('folder_name')
        self.swaption_atm_fwd_rate = kwargs.get('swaption_atm_fwd_rate')
        self.live_date = kwargs.get('live_date')
        self.ask_high = kwargs.get('ask_high')
        self.corporate_action_type = kwargs.get('corporate_action_type')
        self.prime_id = kwargs.get('prime_id')
        self.region_name = kwargs.get('region_name')
        self.description = kwargs.get('description')
        self.asset_classifications_is_country_primary = kwargs.get('asset_classifications_is_country_primary')
        self.value_revised = kwargs.get('value_revised')
        self.adjusted_trade_price = kwargs.get('adjusted_trade_price')
        self.is_adr = kwargs.get('is_adr')
        self.factor = kwargs.get('factor')
        self.days_on_loan = kwargs.get('days_on_loan')
        self.long_conviction_small = kwargs.get('long_conviction_small')
        self.service_id = kwargs.get('service_id')
        self.gsfeer = kwargs.get('gsfeer')
        self.wam = kwargs.get('wam')
        self.wal = kwargs.get('wal')
        self.backtest_id = kwargs.get('backtest_id')
        self.leg_two_index_location = kwargs.get('leg_two_index_location')
        self.g_score = kwargs.get('g_score')
        self.corporate_spread_contribution = kwargs.get('corporate_spread_contribution')
        self.market_value = kwargs.get('market_value')
        self.notional_currency1 = kwargs.get('notional_currency1')
        self.net_debt_to_ebitda = kwargs.get('net_debt_to_ebitda')
        self.notional_currency2 = kwargs.get('notional_currency2')
        self.multiple_score = kwargs.get('multiple_score')
        self.beta_adjusted_exposure = kwargs.get('beta_adjusted_exposure')
        self.dividend_points = kwargs.get('dividend_points')
        self.paid = kwargs.get('paid')
        self.short = kwargs.get('short')
        self.bos_in_ticks_description = kwargs.get('bos_in_ticks_description')
        self.implied_correlation = kwargs.get('implied_correlation')
        self.normalized_performance = kwargs.get('normalized_performance')
        self.cm_id = kwargs.get('cm_id')
        self.taxonomy = kwargs.get('taxonomy')
        self.swaption_vol = kwargs.get('swaption_vol')
        self.dividend_yield = kwargs.get('dividend_yield')
        self.source_origin = kwargs.get('source_origin')
        self.measures = kwargs.get('measures')
        self.total_quantity = kwargs.get('total_quantity')
        self.internal_user = kwargs.get('internal_user')
        self.underlyer = kwargs.get('underlyer')
        self.identifier = kwargs.get('identifier')
        self.price_unit = kwargs.get('price_unit')
        self.redemption_option = kwargs.get('redemption_option')
        self.notional_unit2 = kwargs.get('notional_unit2')
        self.unadjusted_low = kwargs.get('unadjusted_low')
        self.notional_unit1 = kwargs.get('notional_unit1')
        self.sedol = kwargs.get('sedol')
        self.rounding_cost_pnl = kwargs.get('rounding_cost_pnl')
        self.sustain_global = kwargs.get('sustain_global')
        self.portfolio_id = kwargs.get('portfolio_id')
        self.ending_date = kwargs.get('ending_date')
        self.cap_floor_atm_fwd_rate = kwargs.get('cap_floor_atm_fwd_rate')
        self.es_percentile = kwargs.get('es_percentile')
        self.ann_return3_year = kwargs.get('ann_return3_year')
        self.rcic = kwargs.get('rcic')
        self.simon_asset_tags = kwargs.get('simon_asset_tags')
        self.forward_point = kwargs.get('forward_point')
        self.hit_rate_qtd = kwargs.get('hit_rate_qtd')
        self.fci = kwargs.get('fci')
        self.recall_quantity = kwargs.get('recall_quantity')
        self.premium = kwargs.get('premium')
        self.low = kwargs.get('low')
        self.cross_group = kwargs.get('cross_group')
        self.five_day_price_change_bps = kwargs.get('five_day_price_change_bps')
        self.holdings = kwargs.get('holdings')
        self.price_method = kwargs.get('price_method')
        self.quoting_style = kwargs.get('quoting_style')
        self.error_message = kwargs.get('error_message')
        self.mid_price = kwargs.get('mid_price')
        self.sts_em_dm = kwargs.get('sts_em_dm')
        self.tcm_cost_horizon2_day = kwargs.get('tcm_cost_horizon2_day')
        self.pending_loan_count = kwargs.get('pending_loan_count')
        self.price_spot_stop_loss_unit = kwargs.get('price_spot_stop_loss_unit')
        self.queue_in_lots = kwargs.get('queue_in_lots')
        self.price_range_in_ticks_description = kwargs.get('price_range_in_ticks_description')
        self.tender_offer_expiration_date = kwargs.get('tender_offer_expiration_date')
        self.primary_country_ric = kwargs.get('primary_country_ric')
        self.leg_one_fixed_payment = kwargs.get('leg_one_fixed_payment')
        self.option_expiration_frequency = kwargs.get('option_expiration_frequency')
        self.lending_fund_nav_trend = kwargs.get('lending_fund_nav_trend')
        self.tcm_cost_participation_rate5_pct = kwargs.get('tcm_cost_participation_rate5_pct')
        self.is_active = kwargs.get('is_active')
        self.use_machine_learning = kwargs.get('use_machine_learning')
        self.growth_score = kwargs.get('growth_score')
        self.buffer_threshold = kwargs.get('buffer_threshold')
        self.price_forming_continuation_data = kwargs.get('price_forming_continuation_data')
        self.adjusted_short_interest = kwargs.get('adjusted_short_interest')
        self.group = kwargs.get('group')
        self.asset_parameters_strike = kwargs.get('asset_parameters_strike')
        self.asset_parameters_termination_date = kwargs.get('asset_parameters_termination_date')
        self.estimated_spread = kwargs.get('estimated_spread')
        self.asset_parameters_effective_date = kwargs.get('asset_parameters_effective_date')
        self.ann_return10_year = kwargs.get('ann_return10_year')
        self.tcm_cost = kwargs.get('tcm_cost')
        self.sustain_japan = kwargs.get('sustain_japan')
        self.fixed_payment_currency_leg1 = kwargs.get('fixed_payment_currency_leg1')
        self.hedge_tracking_error = kwargs.get('hedge_tracking_error')
        self.fixed_payment_currency_leg2 = kwargs.get('fixed_payment_currency_leg2')
        self.market_cap_category = kwargs.get('market_cap_category')
        self.historical_volume = kwargs.get('historical_volume')
        self.strike_price = kwargs.get('strike_price')
        self.reset_frequency_leg1 = kwargs.get('reset_frequency_leg1')
        self.reset_frequency_leg2 = kwargs.get('reset_frequency_leg2')
        self.equity_gamma = kwargs.get('equity_gamma')
        self.gross_income = kwargs.get('gross_income')
        self.em_id = kwargs.get('em_id')
        self.adjusted_open_price = kwargs.get('adjusted_open_price')
        self.asset_count_in_model = kwargs.get('asset_count_in_model')
        self.sts_credit_region = kwargs.get('sts_credit_region')
        self.country_id = kwargs.get('country_id')
        self.point = kwargs.get('point')
        self.total_returns = kwargs.get('total_returns')
        self.lender = kwargs.get('lender')
        self.ann_return1_year = kwargs.get('ann_return1_year')
        self.min_temperature = kwargs.get('min_temperature')
        self.eff_yield7_day = kwargs.get('eff_yield7_day')
        self.meeting_date = kwargs.get('meeting_date')
        self.relative_strike = kwargs.get('relative_strike')
        self.amount = kwargs.get('amount')
        self.lending_fund_acct = kwargs.get('lending_fund_acct')
        self.rebate = kwargs.get('rebate')
        self.flagship = kwargs.get('flagship')
        self.additional_price_notation = kwargs.get('additional_price_notation')
        self.factor_category = kwargs.get('factor_category')
        self.election_type = kwargs.get('election_type')
        self.implied_volatility = kwargs.get('implied_volatility')
        self.spread = kwargs.get('spread')
        self.equity_delta = kwargs.get('equity_delta')
        self.gross_weight = kwargs.get('gross_weight')
        self.listed = kwargs.get('listed')
        self.variance = kwargs.get('variance')
        self.earnings_record_type = kwargs.get('earnings_record_type')
        self.g10_currency = kwargs.get('g10_currency')
        self.shock_style = kwargs.get('shock_style')
        self.relative_period = kwargs.get('relative_period')
        self.methodology = kwargs.get('methodology')
        self.queue_clock_time_label = kwargs.get('queue_clock_time_label')
        self.market_pnl = kwargs.get('market_pnl')
        self.sustain_asia_ex_japan = kwargs.get('sustain_asia_ex_japan')
        self.asset_classifications_gics_sub_industry = kwargs.get('asset_classifications_gics_sub_industry')
        self.index_leg2 = kwargs.get('index_leg2')
        self.neighbour_asset_id = kwargs.get('neighbour_asset_id')
        self.index_leg1 = kwargs.get('index_leg1')
        self.simon_intl_asset_tags = kwargs.get('simon_intl_asset_tags')
        self.swap_rate = kwargs.get('swap_rate')
        self.path = kwargs.get('path')
        self.client_contact = kwargs.get('client_contact')
        self.rank = kwargs.get('rank')
        self.mixed_swap_other_reported_sdr = kwargs.get('mixed_swap_other_reported_sdr')
        self.data_set_category = kwargs.get('data_set_category')
        self.bos_in_bps_label = kwargs.get('bos_in_bps_label')
        self.bos_in_bps = kwargs.get('bos_in_bps')
        self.point_class = kwargs.get('point_class')
        self.fx_spot = kwargs.get('fx_spot')
        self.bid_low = kwargs.get('bid_low')
        self.restrict_named_individuals = kwargs.get('restrict_named_individuals')
        self.fair_variance_volatility = kwargs.get('fair_variance_volatility')
        self.hedge_volatility = kwargs.get('hedge_volatility')
        self.tags = kwargs.get('tags')
        self.underlying_asset_id = kwargs.get('underlying_asset_id')
        self.real_long_rates_contribution = kwargs.get('real_long_rates_contribution')
        self.client_exposure = kwargs.get('client_exposure')
        self.gs_sustain_sub_sector = kwargs.get('gs_sustain_sub_sector')
        self.domain = kwargs.get('domain')
        self.forward_tenor = kwargs.get('forward_tenor')
        self.jsn = kwargs.get('jsn')
        self.share_class_assets = kwargs.get('share_class_assets')
        self.annuity = kwargs.get('annuity')
        self.quote_type = kwargs.get('quote_type')
        self.uid = kwargs.get('uid')
        self.tenor = kwargs.get('tenor')
        self.es_policy_percentile = kwargs.get('es_policy_percentile')
        self.floating_rate_option = kwargs.get('floating_rate_option')
        self.term = kwargs.get('term')
        self.restrict_internal_gs_ntk = kwargs.get('restrict_internal_gs_ntk')
        self.asset_parameters_clearing_house = kwargs.get('asset_parameters_clearing_house')
        self.tcm_cost_participation_rate100_pct = kwargs.get('tcm_cost_participation_rate100_pct')
        self.disclaimer = kwargs.get('disclaimer')
        self.measure_idx = kwargs.get('measure_idx')
        self.loan_fee = kwargs.get('loan_fee')
        self.deployment_version = kwargs.get('deployment_version')
        self.twi_contribution = kwargs.get('twi_contribution')
        self.delisted = kwargs.get('delisted')
        self.regional_focus = kwargs.get('regional_focus')
        self.volume_primary = kwargs.get('volume_primary')
        self.leg_two_delivery_point = kwargs.get('leg_two_delivery_point')
        self.funding_bid_price = kwargs.get('funding_bid_price')
        self.series = kwargs.get('series')
        self.price_to_sales = kwargs.get('price_to_sales')
        self.closing_auction = kwargs.get('closing_auction')
        self.new_ideas_qtd = kwargs.get('new_ideas_qtd')
        self.adjusted_ask_price = kwargs.get('adjusted_ask_price')
        self.quarter = kwargs.get('quarter')
        self.factor_universe = kwargs.get('factor_universe')
        self.asset_parameters_floating_rate_option = kwargs.get('asset_parameters_floating_rate_option')
        self.arrival_rt = kwargs.get('arrival_rt')
        self.vote_share = kwargs.get('vote_share')
        self.excess_margin_value = kwargs.get('excess_margin_value')
        self.transaction_cost = kwargs.get('transaction_cost')
        self.central_bank_swap_rate = kwargs.get('central_bank_swap_rate')
        self.servicing_cost_short_pnl = kwargs.get('servicing_cost_short_pnl')
        self.notional_unit_leg1 = kwargs.get('notional_unit_leg1')
        self.cluster_description = kwargs.get('cluster_description')
        self.notional_unit_leg2 = kwargs.get('notional_unit_leg2')
        self.position_amount = kwargs.get('position_amount')
        self.wind_speed = kwargs.get('wind_speed')
        self.ma_rank = kwargs.get('ma_rank')
        self.borrower_id = kwargs.get('borrower_id')
        self.data_product = kwargs.get('data_product')
        self.implied_volatility_by_delta_strike = kwargs.get('implied_volatility_by_delta_strike')
        self.mq_symbol = kwargs.get('mq_symbol')
        self.bm_prime_id = kwargs.get('bm_prime_id')
        self.corporate_action = kwargs.get('corporate_action')
        self.conviction = kwargs.get('conviction')
        self.benchmark_maturity = kwargs.get('benchmark_maturity')
        self.gross_flow_normalized = kwargs.get('gross_flow_normalized')
        self.g_regional_score = kwargs.get('g_regional_score')
        self.factor_id = kwargs.get('factor_id')
        self.hard_to_borrow = kwargs.get('hard_to_borrow')
        self.sts_fx_currency = kwargs.get('sts_fx_currency')
        self.wpk = kwargs.get('wpk')
        self.bid_change = kwargs.get('bid_change')
        self.month = kwargs.get('month')
        self.asset_parameters_expiration_date = kwargs.get('asset_parameters_expiration_date')
        self.expiration = kwargs.get('expiration')
        self.country_name = kwargs.get('country_name')
        self.starting_date = kwargs.get('starting_date')
        self.loan_id = kwargs.get('loan_id')
        self.onboarded = kwargs.get('onboarded')
        self.liquidity_score = kwargs.get('liquidity_score')
        self.spread_leg2 = kwargs.get('spread_leg2')
        self.spread_leg1 = kwargs.get('spread_leg1')
        self.long_rates_contribution = kwargs.get('long_rates_contribution')
        self.importance = kwargs.get('importance')
        self.source_date_span = kwargs.get('source_date_span')
        self.asset_classifications_gics_sector = kwargs.get('asset_classifications_gics_sector')
        self.ann_yield6_month = kwargs.get('ann_yield6_month')
        self.underlying_data_set_id = kwargs.get('underlying_data_set_id')
        self.sts_asset_name = kwargs.get('sts_asset_name')
        self.close_unadjusted = kwargs.get('close_unadjusted')
        self.value_unit = kwargs.get('value_unit')
        self.quantity_unit = kwargs.get('quantity_unit')
        self.adjusted_low_price = kwargs.get('adjusted_low_price')
        self.net_exposure_classification = kwargs.get('net_exposure_classification')
        self.settlement_method = kwargs.get('settlement_method')
        self.long_conviction_large = kwargs.get('long_conviction_large')
        self.oad = kwargs.get('oad')
        self.load = kwargs.get('load')
        self.rate = kwargs.get('rate')
        self.alpha = kwargs.get('alpha')
        self.client = kwargs.get('client')
        self.company = kwargs.get('company')
        self.conviction_list = kwargs.get('conviction_list')
        self.settlement_frequency = kwargs.get('settlement_frequency')
        self.dist_avg7_day = kwargs.get('dist_avg7_day')
        self.remove_tape_c = kwargs.get('remove_tape_c')
        self.remove_tape_b = kwargs.get('remove_tape_b')
        self.in_risk_model = kwargs.get('in_risk_model')
        self.daily_net_shareholder_flows_percent = kwargs.get('daily_net_shareholder_flows_percent')
        self.type_of_return = kwargs.get('type_of_return')
        self.servicing_cost_long_pnl = kwargs.get('servicing_cost_long_pnl')
        self.excess_margin_percentage = kwargs.get('excess_margin_percentage')
        self.remove_tape_a = kwargs.get('remove_tape_a')
        self.meeting_number = kwargs.get('meeting_number')
        self.exchange_id = kwargs.get('exchange_id')
        self.mid_gspread = kwargs.get('mid_gspread')
        self.tcm_cost_horizon20_day = kwargs.get('tcm_cost_horizon20_day')
        self.long_level = kwargs.get('long_level')
        self.realm = kwargs.get('realm')
        self.bid = kwargs.get('bid')
        self.data_description = kwargs.get('data_description')
        self.is_aggressive = kwargs.get('is_aggressive')
        self.order_id = kwargs.get('order_id')
        self.gsideid = kwargs.get('gsideid')
        self.repo_rate = kwargs.get('repo_rate')
        self.division = kwargs.get('division')
        self.market_cap_usd = kwargs.get('market_cap_usd')
        self.high_price = kwargs.get('high_price')
        self.absolute_shares = kwargs.get('absolute_shares')
        self.action = kwargs.get('action')
        self.model = kwargs.get('model')
        self.__id = kwargs.get('id_')
        self.arrival_haircut_vwap_normalized = kwargs.get('arrival_haircut_vwap_normalized')
        self.price_component = kwargs.get('price_component')
        self.queue_clock_time_description = kwargs.get('queue_clock_time_description')
        self.delta_strike = kwargs.get('delta_strike')
        self.asset_parameters_notional_currency = kwargs.get('asset_parameters_notional_currency')
        self.value_actual = kwargs.get('value_actual')
        self.upi = kwargs.get('upi')
        self.asset_types = kwargs.get('asset_types')
        self.bcid = kwargs.get('bcid')
        self.mkt_point = kwargs.get('mkt_point')
        self.collateral_currency = kwargs.get('collateral_currency')
        self.original_country = kwargs.get('original_country')
        self.touch_liquidity_score = kwargs.get('touch_liquidity_score')
        self.field = kwargs.get('field')
        self.factor_category_id = kwargs.get('factor_category_id')
        self.expected_completion_date = kwargs.get('expected_completion_date')
        self.spread_option_vol = kwargs.get('spread_option_vol')
        self.inflation_swap_rate = kwargs.get('inflation_swap_rate')
        self.fx_risk_premium_index = kwargs.get('fx_risk_premium_index')
        self.skew = kwargs.get('skew')
        self.status = kwargs.get('status')
        self.sustain_emerging_markets = kwargs.get('sustain_emerging_markets')
        self.total_price = kwargs.get('total_price')
        self.embeded_option = kwargs.get('embeded_option')
        self.event_source = kwargs.get('event_source')
        self.on_behalf_of = kwargs.get('on_behalf_of')
        self.qis_perm_no = kwargs.get('qis_perm_no')
        self.shareclass_id = kwargs.get('shareclass_id')
        self.sts_commodity_sector = kwargs.get('sts_commodity_sector')
        self.exception_status = kwargs.get('exception_status')
        self.sales_coverage = kwargs.get('sales_coverage')
        self.short_exposure = kwargs.get('short_exposure')
        self.tcm_cost_participation_rate10_pct = kwargs.get('tcm_cost_participation_rate10_pct')
        self.event_time = kwargs.get('event_time')
        self.position_source_name = kwargs.get('position_source_name')
        self.arrival_haircut_vwap = kwargs.get('arrival_haircut_vwap')
        self.interest_rate = kwargs.get('interest_rate')
        self.execution_days = kwargs.get('execution_days')
        self.side = kwargs.get('side')
        self.compliance_restricted_status = kwargs.get('compliance_restricted_status')
        self.forward = kwargs.get('forward')
        self.borrow_fee = kwargs.get('borrow_fee')
        self.strike = kwargs.get('strike')
        self.loan_spread = kwargs.get('loan_spread')
        self.tcm_cost_horizon12_hour = kwargs.get('tcm_cost_horizon12_hour')
        self.dew_point = kwargs.get('dew_point')
        self.research_commission = kwargs.get('research_commission')
        self.leg_one_delivery_point = kwargs.get('leg_one_delivery_point')
        self.asset_classifications_risk_country_code = kwargs.get('asset_classifications_risk_country_code')
        self.event_status = kwargs.get('event_status')
        self.asset_parameters_settlement = kwargs.get('asset_parameters_settlement')
        self.__return = kwargs.get('return_')
        self.max_temperature = kwargs.get('max_temperature')
        self.acquirer_shareholder_meeting_date = kwargs.get('acquirer_shareholder_meeting_date')
        self.notional_amount = kwargs.get('notional_amount')
        self.pay_or_receive = kwargs.get('pay_or_receive')
        self.arrival_rt_normalized = kwargs.get('arrival_rt_normalized')
        self.report_type = kwargs.get('report_type')
        self.source_url = kwargs.get('source_url')
        self.estimated_return = kwargs.get('estimated_return')
        self.high = kwargs.get('high')
        self.source_last_update = kwargs.get('source_last_update')
        self.quantity_mw = kwargs.get('quantity_mw')
        self.pnode_id = kwargs.get('pnode_id')
        self.event_name = kwargs.get('event_name')
        self.indication_of_other_price_affecting_term = kwargs.get('indication_of_other_price_affecting_term')
        self.unadjusted_bid = kwargs.get('unadjusted_bid')
        self.backtest_type = kwargs.get('backtest_type')
        self.gsdeer = kwargs.get('gsdeer')
        self.g_regional_percentile = kwargs.get('g_regional_percentile')
        self.prev_close_ask = kwargs.get('prev_close_ask')
        self.level = kwargs.get('level')
        self.mnav = kwargs.get('mnav')
        self.es_momentum_score = kwargs.get('es_momentum_score')
        self.curr_yield7_day = kwargs.get('curr_yield7_day')
        self.pressure = kwargs.get('pressure')
        self.short_description = kwargs.get('short_description')
        self.feed = kwargs.get('feed')
        self.net_weight = kwargs.get('net_weight')
        self.portfolio_managers = kwargs.get('portfolio_managers')
        self.asset_parameters_commodity_sector = kwargs.get('asset_parameters_commodity_sector')
        self.bos_in_ticks = kwargs.get('bos_in_ticks')
        self.price_notation2 = kwargs.get('price_notation2')
        self.market_buffer_threshold = kwargs.get('market_buffer_threshold')
        self.price_notation3 = kwargs.get('price_notation3')
        self.cap_floor_vol = kwargs.get('cap_floor_vol')
        self.submitter = kwargs.get('submitter')
        self.notional = kwargs.get('notional')
        self.es_disclosure_percentage = kwargs.get('es_disclosure_percentage')
        self.investment_income = kwargs.get('investment_income')
        self.forward_point_imm = kwargs.get('forward_point_imm')
        self.client_short_name = kwargs.get('client_short_name')
        self.group_category = kwargs.get('group_category')
        self.bid_plus_ask = kwargs.get('bid_plus_ask')
        self.foreign_ccy_rate = kwargs.get('foreign_ccy_rate')
        self.election_odds = kwargs.get('election_odds')
        self.require_anon_client_name = kwargs.get('require_anon_client_name')
        self.total = kwargs.get('total')
        self.asset_id = kwargs.get('asset_id')
        self.mkt_type = kwargs.get('mkt_type')
        self.pricing_location = kwargs.get('pricing_location')
        self.yield30_day = kwargs.get('yield30_day')
        self.proportion_of_risk = kwargs.get('proportion_of_risk')
        self.beta = kwargs.get('beta')
        self.long_exposure = kwargs.get('long_exposure')
        self.tcm_cost_participation_rate20_pct = kwargs.get('tcm_cost_participation_rate20_pct')
        self.multi_asset_class_swap = kwargs.get('multi_asset_class_swap')
        self.cross = kwargs.get('cross')
        self.idea_status = kwargs.get('idea_status')
        self.contract_subtype = kwargs.get('contract_subtype')
        self.fx_forecast = kwargs.get('fx_forecast')
        self.fixing_time_label = kwargs.get('fixing_time_label')
        self.implementation_id = kwargs.get('implementation_id')
        self.fill_id = kwargs.get('fill_id')
        self.excess_returns = kwargs.get('excess_returns')
        self.dollar_return = kwargs.get('dollar_return')
        self.es_numeric_score = kwargs.get('es_numeric_score')
        self.in_benchmark = kwargs.get('in_benchmark')
        self.return_on_equity = kwargs.get('return_on_equity')
        self.action_sdr = kwargs.get('action_sdr')
        self.queue_in_lots_description = kwargs.get('queue_in_lots_description')
        self.objective = kwargs.get('objective')
        self.nav_price = kwargs.get('nav_price')
        self.precipitation = kwargs.get('precipitation')
        self.hedge_notional = kwargs.get('hedge_notional')
        self.ask_low = kwargs.get('ask_low')
        self.beta_adjusted_net_exposure = kwargs.get('beta_adjusted_net_exposure')
        self.expiry = kwargs.get('expiry')
        self.avg_monthly_yield = kwargs.get('avg_monthly_yield')
        self.period_direction = kwargs.get('period_direction')
        self.earnings_per_share = kwargs.get('earnings_per_share')
        self.strike_percentage = kwargs.get('strike_percentage')
        self.excess_return_price = kwargs.get('excess_return_price')
        self.prev_close_bid = kwargs.get('prev_close_bid')
        self.fx_pnl = kwargs.get('fx_pnl')
        self.tcm_cost_horizon16_day = kwargs.get('tcm_cost_horizon16_day')
        self.sales_per_share = kwargs.get('sales_per_share')
        self.asset_classifications_gics_industry_group = kwargs.get('asset_classifications_gics_industry_group')
        self.unadjusted_close = kwargs.get('unadjusted_close')
        self.lending_sec_id = kwargs.get('lending_sec_id')
        self.equity_theta = kwargs.get('equity_theta')
        self.execution_fee = kwargs.get('execution_fee')
        self.collateral_percentage_actual = kwargs.get('collateral_percentage_actual')
        self.mixed_swap = kwargs.get('mixed_swap')
        self.snowfall = kwargs.get('snowfall')
        self.mic = kwargs.get('mic')
        self.mid = kwargs.get('mid')
        self.auto_exec_state = kwargs.get('auto_exec_state')
        self.relative_return_ytd = kwargs.get('relative_return_ytd')
        self.long = kwargs.get('long')
        self.region_code = kwargs.get('region_code')
        self.long_weight = kwargs.get('long_weight')
        self.calculation_time = kwargs.get('calculation_time')
        self.real_time_restriction_status = kwargs.get('real_time_restriction_status')
        self.average_realized_variance = kwargs.get('average_realized_variance')
        self.financial_returns_score = kwargs.get('financial_returns_score')
        self.year_or_quarter = kwargs.get('year_or_quarter')
        self.settlement_type = kwargs.get('settlement_type')
        self.net_change = kwargs.get('net_change')
        self.non_symbol_dimensions = kwargs.get('non_symbol_dimensions')
        self.leg_two_fixed_payment_currency = kwargs.get('leg_two_fixed_payment_currency')
        self.number_of_underliers = kwargs.get('number_of_underliers')
        self.swap_type = kwargs.get('swap_type')
        self.forecast_type = kwargs.get('forecast_type')
        self.asset_classifications_country_name = kwargs.get('asset_classifications_country_name')
        self.new_ideas_ytd = kwargs.get('new_ideas_ytd')
        self.management_fee = kwargs.get('management_fee')
        self.__open = kwargs.get('open_')
        self.source_id = kwargs.get('source_id')
        self.country = kwargs.get('country')
        self.cusip = kwargs.get('cusip')
        self.touch_spread_score = kwargs.get('touch_spread_score')
        self.spread_option_atm_fwd_rate = kwargs.get('spread_option_atm_fwd_rate')
        self.net_exposure = kwargs.get('net_exposure')
        self.frequency = kwargs.get('frequency')
        self.activity_id = kwargs.get('activity_id')
        self.estimated_impact = kwargs.get('estimated_impact')
        self.loan_spread_bucket = kwargs.get('loan_spread_bucket')
        self.asset_parameters_pricing_location = kwargs.get('asset_parameters_pricing_location')
        self.event_description = kwargs.get('event_description')
        self.provide_non_display_tape_a = kwargs.get('provide_non_display_tape_a')
        self.strike_reference = kwargs.get('strike_reference')
        self.details = kwargs.get('details')
        self.provide_non_display_tape_c = kwargs.get('provide_non_display_tape_c')
        self.asset_count = kwargs.get('asset_count')
        self.provide_non_display_tape_b = kwargs.get('provide_non_display_tape_b')
        self.sector = kwargs.get('sector')
        self.fundamental_metric = kwargs.get('fundamental_metric')
        self.absolute_value = kwargs.get('absolute_value')
        self.closing_report = kwargs.get('closing_report')
        self.long_tenor = kwargs.get('long_tenor')
        self.mctr = kwargs.get('mctr')
        self.historical_close = kwargs.get('historical_close')
        self.asset_count_priced = kwargs.get('asset_count_priced')
        self.idea_id = kwargs.get('idea_id')
        self.comment_status = kwargs.get('comment_status')
        self.marginal_cost = kwargs.get('marginal_cost')
        self.settlement_currency = kwargs.get('settlement_currency')
        self.client_weight = kwargs.get('client_weight')
        self.indication_of_collateralization = kwargs.get('indication_of_collateralization')
        self.liq_wkly = kwargs.get('liq_wkly')
        self.lending_partner_fee = kwargs.get('lending_partner_fee')
        self.region = kwargs.get('region')
        self.tenor2 = kwargs.get('tenor2')
        self.option_premium = kwargs.get('option_premium')
        self.owner_name = kwargs.get('owner_name')
        self.last_updated_by_id = kwargs.get('last_updated_by_id')
        self.z_score = kwargs.get('z_score')
        self.legal_entity_acct = kwargs.get('legal_entity_acct')
        self.target_shareholder_meeting_date = kwargs.get('target_shareholder_meeting_date')
        self.event_start_time = kwargs.get('event_start_time')
        self.turnover = kwargs.get('turnover')
        self.price_spot_target_unit = kwargs.get('price_spot_target_unit')
        self.leg_one_type = kwargs.get('leg_one_type')
        self.leg_two_spread = kwargs.get('leg_two_spread')
        self.coverage = kwargs.get('coverage')
        self.g_percentile = kwargs.get('g_percentile')
        self.lending_fund_nav = kwargs.get('lending_fund_nav')
        self.source_original_category = kwargs.get('source_original_category')
        self.composite5_day_adv = kwargs.get('composite5_day_adv')
        self.marginal_contribution_to_risk = kwargs.get('marginal_contribution_to_risk')
        self.new_ideas_wtd = kwargs.get('new_ideas_wtd')
        self.asset_class_sdr = kwargs.get('asset_class_sdr')
        self.location = kwargs.get('location')
        self.comment = kwargs.get('comment')
        self.source_symbol = kwargs.get('source_symbol')
        self.scenario_id = kwargs.get('scenario_id')
        self.ask_unadjusted = kwargs.get('ask_unadjusted')
        self.termination_tenor = kwargs.get('termination_tenor')
        self.queue_clock_time = kwargs.get('queue_clock_time')
        self.restrict_external_derived_data = kwargs.get('restrict_external_derived_data')
        self.ask_change = kwargs.get('ask_change')
        self.tcm_cost_participation_rate50_pct = kwargs.get('tcm_cost_participation_rate50_pct')
        self.contract_type = kwargs.get('contract_type')
        self.forward_price = kwargs.get('forward_price')
        self.__type = kwargs.get('type_')
        self.strike_ref = kwargs.get('strike_ref')
        self.mdapi = kwargs.get('mdapi')
        self.cumulative_pnl = kwargs.get('cumulative_pnl')
        self.short_tenor = kwargs.get('short_tenor')
        self.loss = kwargs.get('loss')
        self.unadjusted_volume = kwargs.get('unadjusted_volume')
        self.midcurve_vol = kwargs.get('midcurve_vol')
        self.trading_cost_pnl = kwargs.get('trading_cost_pnl')
        self.price_notation_type = kwargs.get('price_notation_type')
        self.price = kwargs.get('price')
        self.payment_quantity = kwargs.get('payment_quantity')
        self.position_idx = kwargs.get('position_idx')
        self.sec_name = kwargs.get('sec_name')
        self.implied_volatility_by_relative_strike = kwargs.get('implied_volatility_by_relative_strike')
        self.percent_adv = kwargs.get('percent_adv')
        self.sub_region = kwargs.get('sub_region')
        self.contract = kwargs.get('contract')
        self.payment_frequency1 = kwargs.get('payment_frequency1')
        self.payment_frequency2 = kwargs.get('payment_frequency2')
        self.bespoke = kwargs.get('bespoke')
        self.repo_tenor = kwargs.get('repo_tenor')
        self.quality_stars = kwargs.get('quality_stars')
        self.source_ticker = kwargs.get('source_ticker')
        self.gsid = kwargs.get('gsid')
        self.lending_fund = kwargs.get('lending_fund')
        self.tcm_cost_participation_rate15_pct = kwargs.get('tcm_cost_participation_rate15_pct')
        self.sensitivity = kwargs.get('sensitivity')
        self.fiscal_year = kwargs.get('fiscal_year')
        self.internal = kwargs.get('internal')
        self.asset_classifications_gics_industry = kwargs.get('asset_classifications_gics_industry')
        self.adjusted_bid_price = kwargs.get('adjusted_bid_price')
        self.var_swap = kwargs.get('var_swap')
        self.fixed_payment_leg2 = kwargs.get('fixed_payment_leg2')
        self.fixed_payment_leg1 = kwargs.get('fixed_payment_leg1')
        self.low_unadjusted = kwargs.get('low_unadjusted')
        self.original_dissemination_id = kwargs.get('original_dissemination_id')
        self.macs_secondary_asset_class = kwargs.get('macs_secondary_asset_class')
        self.leg_two_averaging_method = kwargs.get('leg_two_averaging_method')
        self.sectors_raw = kwargs.get('sectors_raw')
        self.shareclass_price = kwargs.get('shareclass_price')
        self.integrated_score = kwargs.get('integrated_score')
        self.trade_size = kwargs.get('trade_size')
        self.price_spot_entry_value = kwargs.get('price_spot_entry_value')
        self.symbol_dimensions = kwargs.get('symbol_dimensions')
        self.index_location_leg1 = kwargs.get('index_location_leg1')
        self.index_location_leg2 = kwargs.get('index_location_leg2')
        self.option_type_sdr = kwargs.get('option_type_sdr')
        self.scenario_group_id = kwargs.get('scenario_group_id')
        self.avg_yield7_day = kwargs.get('avg_yield7_day')
        self.average_implied_variance = kwargs.get('average_implied_variance')
        self.averaging_method_leg2 = kwargs.get('averaging_method_leg2')
        self.avg_trade_rate_description = kwargs.get('avg_trade_rate_description')
        self.averaging_method_leg1 = kwargs.get('averaging_method_leg1')
        self.fraction = kwargs.get('fraction')
        self.sts_credit_market = kwargs.get('sts_credit_market')
        self.asset_count_short = kwargs.get('asset_count_short')
        self.collateral_percentage_required = kwargs.get('collateral_percentage_required')
        self.opening_auction = kwargs.get('opening_auction')
        self.total_std_return_since_inception = kwargs.get('total_std_return_since_inception')
        self.high_unadjusted = kwargs.get('high_unadjusted')
        self.source_category = kwargs.get('source_category')
        self.tv_product_mnemonic = kwargs.get('tv_product_mnemonic')
        self.volume_unadjusted = kwargs.get('volume_unadjusted')
        self.price_to_earnings = kwargs.get('price_to_earnings')
        self.avg_trade_rate_label = kwargs.get('avg_trade_rate_label')
        self.ann_yield3_month = kwargs.get('ann_yield3_month')
        self.net_flow_std = kwargs.get('net_flow_std')
        self.encoded_stats = kwargs.get('encoded_stats')
        self.ask_size = kwargs.get('ask_size')
        self.std30_days_unsubsidized_yield = kwargs.get('std30_days_unsubsidized_yield')
        self.resource = kwargs.get('resource')
        self.price_to_cash = kwargs.get('price_to_cash')
        self.average_realized_volatility = kwargs.get('average_realized_volatility')
        self.nav_spread = kwargs.get('nav_spread')
        self.bid_price = kwargs.get('bid_price')
        self.dollar_total_return = kwargs.get('dollar_total_return')
        self.block_unit = kwargs.get('block_unit')
        self.es_numeric_percentile = kwargs.get('es_numeric_percentile')
        self.repurchase_rate = kwargs.get('repurchase_rate')
        self.csa_terms = kwargs.get('csa_terms')
        self.daily_net_shareholder_flows = kwargs.get('daily_net_shareholder_flows')
        self.ask_gspread = kwargs.get('ask_gspread')
        self.cal_spread_mis_pricing = kwargs.get('cal_spread_mis_pricing')
        self.leg_two_type = kwargs.get('leg_two_type')
        self.rate366 = kwargs.get('rate366')
        self.rate365 = kwargs.get('rate365')
        self.rate360 = kwargs.get('rate360')
        self.delivery_point_leg1 = kwargs.get('delivery_point_leg1')
        self.opening_report = kwargs.get('opening_report')
        self.value = kwargs.get('value')
        self.leg_one_index_location = kwargs.get('leg_one_index_location')
        self.product_type = kwargs.get('product_type')
        self.quantity = kwargs.get('quantity')
        self.report_id = kwargs.get('report_id')
        self.index_weight = kwargs.get('index_weight')
        self.macs_primary_asset_class = kwargs.get('macs_primary_asset_class')
        self.midcurve_atm_fwd_rate = kwargs.get('midcurve_atm_fwd_rate')
        self.trader = kwargs.get('trader')
        self.equity_risk_premium_index = kwargs.get('equity_risk_premium_index')
        self.clearing_house = kwargs.get('clearing_house')
        self.sts_rates_maturity = kwargs.get('sts_rates_maturity')
        self.valuation_date = kwargs.get('valuation_date')
        self.restrict_gs_federation = kwargs.get('restrict_gs_federation')
        self.position_source = kwargs.get('position_source')
        self.tcm_cost_horizon6_hour = kwargs.get('tcm_cost_horizon6_hour')
        self.liq_dly = kwargs.get('liq_dly')
        self.price_to_book = kwargs.get('price_to_book')
        self.isin = kwargs.get('isin')

    @property
    def collateral_value_variance(self) -> dict:
        return self.__collateral_value_variance

    @collateral_value_variance.setter
    def collateral_value_variance(self, value: dict):
        self._property_changed('collateral_value_variance')
        self.__collateral_value_variance = value        

    @property
    def year(self) -> dict:
        return self.__year

    @year.setter
    def year(self, value: dict):
        self._property_changed('year')
        self.__year = value        

    @property
    def investment_rate(self) -> dict:
        return self.__investment_rate

    @investment_rate.setter
    def investment_rate(self, value: dict):
        self._property_changed('investment_rate')
        self.__investment_rate = value        

    @property
    def forecast_period(self) -> dict:
        return self.__forecast_period

    @forecast_period.setter
    def forecast_period(self, value: dict):
        self._property_changed('forecast_period')
        self.__forecast_period = value        

    @property
    def mdapi_class(self) -> dict:
        return self.__mdapi_class

    @mdapi_class.setter
    def mdapi_class(self, value: dict):
        self._property_changed('mdapi_class')
        self.__mdapi_class = value        

    @property
    def data_set_ids(self) -> dict:
        return self.__data_set_ids

    @data_set_ids.setter
    def data_set_ids(self, value: dict):
        self._property_changed('data_set_ids')
        self.__data_set_ids = value        

    @property
    def bid_unadjusted(self) -> dict:
        return self.__bid_unadjusted

    @bid_unadjusted.setter
    def bid_unadjusted(self, value: dict):
        self._property_changed('bid_unadjusted')
        self.__bid_unadjusted = value        

    @property
    def economic_terms_hash(self) -> dict:
        return self.__economic_terms_hash

    @economic_terms_hash.setter
    def economic_terms_hash(self, value: dict):
        self._property_changed('economic_terms_hash')
        self.__economic_terms_hash = value        

    @property
    def client_type(self) -> dict:
        return self.__client_type

    @client_type.setter
    def client_type(self, value: dict):
        self._property_changed('client_type')
        self.__client_type = value        

    @property
    def available_inventory(self) -> dict:
        return self.__available_inventory

    @available_inventory.setter
    def available_inventory(self, value: dict):
        self._property_changed('available_inventory')
        self.__available_inventory = value        

    @property
    def est1_day_complete_pct(self) -> dict:
        return self.__est1_day_complete_pct

    @est1_day_complete_pct.setter
    def est1_day_complete_pct(self, value: dict):
        self._property_changed('est1_day_complete_pct')
        self.__est1_day_complete_pct = value        

    @property
    def created_by_id(self) -> dict:
        return self.__created_by_id

    @created_by_id.setter
    def created_by_id(self, value: dict):
        self._property_changed('created_by_id')
        self.__created_by_id = value        

    @property
    def vehicle_type(self) -> dict:
        return self.__vehicle_type

    @vehicle_type.setter
    def vehicle_type(self, value: dict):
        self._property_changed('vehicle_type')
        self.__vehicle_type = value        

    @property
    def daily_risk(self) -> dict:
        return self.__daily_risk

    @daily_risk.setter
    def daily_risk(self, value: dict):
        self._property_changed('daily_risk')
        self.__daily_risk = value        

    @property
    def energy(self) -> dict:
        return self.__energy

    @energy.setter
    def energy(self, value: dict):
        self._property_changed('energy')
        self.__energy = value        

    @property
    def market_data_type(self) -> dict:
        return self.__market_data_type

    @market_data_type.setter
    def market_data_type(self, value: dict):
        self._property_changed('market_data_type')
        self.__market_data_type = value        

    @property
    def real_short_rates_contribution(self) -> dict:
        return self.__real_short_rates_contribution

    @real_short_rates_contribution.setter
    def real_short_rates_contribution(self, value: dict):
        self._property_changed('real_short_rates_contribution')
        self.__real_short_rates_contribution = value        

    @property
    def sentiment_score(self) -> dict:
        return self.__sentiment_score

    @sentiment_score.setter
    def sentiment_score(self, value: dict):
        self._property_changed('sentiment_score')
        self.__sentiment_score = value        

    @property
    def leg_one_payment_type(self) -> dict:
        return self.__leg_one_payment_type

    @leg_one_payment_type.setter
    def leg_one_payment_type(self, value: dict):
        self._property_changed('leg_one_payment_type')
        self.__leg_one_payment_type = value        

    @property
    def provide_tape_c(self) -> dict:
        return self.__provide_tape_c

    @provide_tape_c.setter
    def provide_tape_c(self, value: dict):
        self._property_changed('provide_tape_c')
        self.__provide_tape_c = value        

    @property
    def value_previous(self) -> dict:
        return self.__value_previous

    @value_previous.setter
    def value_previous(self, value: dict):
        self._property_changed('value_previous')
        self.__value_previous = value        

    @property
    def delivery_point_leg2(self) -> dict:
        return self.__delivery_point_leg2

    @delivery_point_leg2.setter
    def delivery_point_leg2(self, value: dict):
        self._property_changed('delivery_point_leg2')
        self.__delivery_point_leg2 = value        

    @property
    def avg_trade_rate(self) -> dict:
        return self.__avg_trade_rate

    @avg_trade_rate.setter
    def avg_trade_rate(self, value: dict):
        self._property_changed('avg_trade_rate')
        self.__avg_trade_rate = value        

    @property
    def short_level(self) -> dict:
        return self.__short_level

    @short_level.setter
    def short_level(self, value: dict):
        self._property_changed('short_level')
        self.__short_level = value        

    @property
    def version(self) -> dict:
        return self.__version

    @version.setter
    def version(self, value: dict):
        self._property_changed('version')
        self.__version = value        

    @property
    def policy_rate_expectation(self) -> dict:
        return self.__policy_rate_expectation

    @policy_rate_expectation.setter
    def policy_rate_expectation(self, value: dict):
        self._property_changed('policy_rate_expectation')
        self.__policy_rate_expectation = value        

    @property
    def correlation(self) -> dict:
        return self.__correlation

    @correlation.setter
    def correlation(self, value: dict):
        self._property_changed('correlation')
        self.__correlation = value        

    @property
    def exposure(self) -> dict:
        return self.__exposure

    @exposure.setter
    def exposure(self, value: dict):
        self._property_changed('exposure')
        self.__exposure = value        

    @property
    def market_data_asset(self) -> dict:
        return self.__market_data_asset

    @market_data_asset.setter
    def market_data_asset(self, value: dict):
        self._property_changed('market_data_asset')
        self.__market_data_asset = value        

    @property
    def earnings_per_share_positive(self) -> dict:
        return self.__earnings_per_share_positive

    @earnings_per_share_positive.setter
    def earnings_per_share_positive(self, value: dict):
        self._property_changed('earnings_per_share_positive')
        self.__earnings_per_share_positive = value        

    @property
    def unadjusted_high(self) -> dict:
        return self.__unadjusted_high

    @unadjusted_high.setter
    def unadjusted_high(self, value: dict):
        self._property_changed('unadjusted_high')
        self.__unadjusted_high = value        

    @property
    def source_importance(self) -> dict:
        return self.__source_importance

    @source_importance.setter
    def source_importance(self, value: dict):
        self._property_changed('source_importance')
        self.__source_importance = value        

    @property
    def eid(self) -> dict:
        return self.__eid

    @eid.setter
    def eid(self, value: dict):
        self._property_changed('eid')
        self.__eid = value        

    @property
    def relative_return_qtd(self) -> dict:
        return self.__relative_return_qtd

    @relative_return_qtd.setter
    def relative_return_qtd(self, value: dict):
        self._property_changed('relative_return_qtd')
        self.__relative_return_qtd = value        

    @property
    def display_name(self) -> dict:
        return self.__display_name

    @display_name.setter
    def display_name(self, value: dict):
        self._property_changed('display_name')
        self.__display_name = value        

    @property
    def minutes_to_trade100_pct(self) -> dict:
        return self.__minutes_to_trade100_pct

    @minutes_to_trade100_pct.setter
    def minutes_to_trade100_pct(self, value: dict):
        self._property_changed('minutes_to_trade100_pct')
        self.__minutes_to_trade100_pct = value        

    @property
    def mkt_quoting_style(self) -> dict:
        return self.__mkt_quoting_style

    @mkt_quoting_style.setter
    def mkt_quoting_style(self, value: dict):
        self._property_changed('mkt_quoting_style')
        self.__mkt_quoting_style = value        

    @property
    def expiration_tenor(self) -> dict:
        return self.__expiration_tenor

    @expiration_tenor.setter
    def expiration_tenor(self, value: dict):
        self._property_changed('expiration_tenor')
        self.__expiration_tenor = value        

    @property
    def market_model_id(self) -> dict:
        return self.__market_model_id

    @market_model_id.setter
    def market_model_id(self, value: dict):
        self._property_changed('market_model_id')
        self.__market_model_id = value        

    @property
    def realized_correlation(self) -> dict:
        return self.__realized_correlation

    @realized_correlation.setter
    def realized_correlation(self, value: dict):
        self._property_changed('realized_correlation')
        self.__realized_correlation = value        

    @property
    def collateral_value_actual(self) -> dict:
        return self.__collateral_value_actual

    @collateral_value_actual.setter
    def collateral_value_actual(self, value: dict):
        self._property_changed('collateral_value_actual')
        self.__collateral_value_actual = value        

    @property
    def upfront_payment(self) -> dict:
        return self.__upfront_payment

    @upfront_payment.setter
    def upfront_payment(self, value: dict):
        self._property_changed('upfront_payment')
        self.__upfront_payment = value        

    @property
    def atm_fwd_rate(self) -> dict:
        return self.__atm_fwd_rate

    @atm_fwd_rate.setter
    def atm_fwd_rate(self, value: dict):
        self._property_changed('atm_fwd_rate')
        self.__atm_fwd_rate = value        

    @property
    def provide_tape_a(self) -> dict:
        return self.__provide_tape_a

    @provide_tape_a.setter
    def provide_tape_a(self, value: dict):
        self._property_changed('provide_tape_a')
        self.__provide_tape_a = value        

    @property
    def provide_tape_b(self) -> dict:
        return self.__provide_tape_b

    @provide_tape_b.setter
    def provide_tape_b(self, value: dict):
        self._property_changed('provide_tape_b')
        self.__provide_tape_b = value        

    @property
    def tcm_cost_participation_rate75_pct(self) -> dict:
        return self.__tcm_cost_participation_rate75_pct

    @tcm_cost_participation_rate75_pct.setter
    def tcm_cost_participation_rate75_pct(self, value: dict):
        self._property_changed('tcm_cost_participation_rate75_pct')
        self.__tcm_cost_participation_rate75_pct = value        

    @property
    def close(self) -> dict:
        return self.__close

    @close.setter
    def close(self, value: dict):
        self._property_changed('close')
        self.__close = value        

    @property
    def a(self) -> dict:
        return self.__a

    @a.setter
    def a(self, value: dict):
        self._property_changed('a')
        self.__a = value        

    @property
    def b(self) -> dict:
        return self.__b

    @b.setter
    def b(self, value: dict):
        self._property_changed('b')
        self.__b = value        

    @property
    def c(self) -> dict:
        return self.__c

    @c.setter
    def c(self, value: dict):
        self._property_changed('c')
        self.__c = value        

    @property
    def equity_vega(self) -> dict:
        return self.__equity_vega

    @equity_vega.setter
    def equity_vega(self, value: dict):
        self._property_changed('equity_vega')
        self.__equity_vega = value        

    @property
    def leg_one_spread(self) -> dict:
        return self.__leg_one_spread

    @leg_one_spread.setter
    def leg_one_spread(self, value: dict):
        self._property_changed('leg_one_spread')
        self.__leg_one_spread = value        

    @property
    def lender_payment(self) -> dict:
        return self.__lender_payment

    @lender_payment.setter
    def lender_payment(self, value: dict):
        self._property_changed('lender_payment')
        self.__lender_payment = value        

    @property
    def five_day_move(self) -> dict:
        return self.__five_day_move

    @five_day_move.setter
    def five_day_move(self, value: dict):
        self._property_changed('five_day_move')
        self.__five_day_move = value        

    @property
    def geography_name(self) -> dict:
        return self.__geography_name

    @geography_name.setter
    def geography_name(self, value: dict):
        self._property_changed('geography_name')
        self.__geography_name = value        

    @property
    def borrower(self) -> dict:
        return self.__borrower

    @borrower.setter
    def borrower(self, value: dict):
        self._property_changed('borrower')
        self.__borrower = value        

    @property
    def value_format(self) -> dict:
        return self.__value_format

    @value_format.setter
    def value_format(self, value: dict):
        self._property_changed('value_format')
        self.__value_format = value        

    @property
    def performance_contribution(self) -> dict:
        return self.__performance_contribution

    @performance_contribution.setter
    def performance_contribution(self, value: dict):
        self._property_changed('performance_contribution')
        self.__performance_contribution = value        

    @property
    def target_notional(self) -> dict:
        return self.__target_notional

    @target_notional.setter
    def target_notional(self, value: dict):
        self._property_changed('target_notional')
        self.__target_notional = value        

    @property
    def fill_leg_id(self) -> dict:
        return self.__fill_leg_id

    @fill_leg_id.setter
    def fill_leg_id(self, value: dict):
        self._property_changed('fill_leg_id')
        self.__fill_leg_id = value        

    @property
    def rationale(self) -> dict:
        return self.__rationale

    @rationale.setter
    def rationale(self, value: dict):
        self._property_changed('rationale')
        self.__rationale = value        

    @property
    def mkt_class(self) -> dict:
        return self.__mkt_class

    @mkt_class.setter
    def mkt_class(self, value: dict):
        self._property_changed('mkt_class')
        self.__mkt_class = value        

    @property
    def last_updated_since(self) -> dict:
        return self.__last_updated_since

    @last_updated_since.setter
    def last_updated_since(self, value: dict):
        self._property_changed('last_updated_since')
        self.__last_updated_since = value        

    @property
    def equities_contribution(self) -> dict:
        return self.__equities_contribution

    @equities_contribution.setter
    def equities_contribution(self, value: dict):
        self._property_changed('equities_contribution')
        self.__equities_contribution = value        

    @property
    def simon_id(self) -> dict:
        return self.__simon_id

    @simon_id.setter
    def simon_id(self, value: dict):
        self._property_changed('simon_id')
        self.__simon_id = value        

    @property
    def congestion(self) -> dict:
        return self.__congestion

    @congestion.setter
    def congestion(self, value: dict):
        self._property_changed('congestion')
        self.__congestion = value        

    @property
    def event_category(self) -> dict:
        return self.__event_category

    @event_category.setter
    def event_category(self, value: dict):
        self._property_changed('event_category')
        self.__event_category = value        

    @property
    def short_rates_contribution(self) -> dict:
        return self.__short_rates_contribution

    @short_rates_contribution.setter
    def short_rates_contribution(self, value: dict):
        self._property_changed('short_rates_contribution')
        self.__short_rates_contribution = value        

    @property
    def implied_normal_volatility(self) -> dict:
        return self.__implied_normal_volatility

    @implied_normal_volatility.setter
    def implied_normal_volatility(self, value: dict):
        self._property_changed('implied_normal_volatility')
        self.__implied_normal_volatility = value        

    @property
    def unadjusted_open(self) -> dict:
        return self.__unadjusted_open

    @unadjusted_open.setter
    def unadjusted_open(self, value: dict):
        self._property_changed('unadjusted_open')
        self.__unadjusted_open = value        

    @property
    def criticality(self) -> dict:
        return self.__criticality

    @criticality.setter
    def criticality(self, value: dict):
        self._property_changed('criticality')
        self.__criticality = value        

    @property
    def mtm_price(self) -> dict:
        return self.__mtm_price

    @mtm_price.setter
    def mtm_price(self, value: dict):
        self._property_changed('mtm_price')
        self.__mtm_price = value        

    @property
    def bid_ask_spread(self) -> dict:
        return self.__bid_ask_spread

    @bid_ask_spread.setter
    def bid_ask_spread(self, value: dict):
        self._property_changed('bid_ask_spread')
        self.__bid_ask_spread = value        

    @property
    def leg_one_averaging_method(self) -> dict:
        return self.__leg_one_averaging_method

    @leg_one_averaging_method.setter
    def leg_one_averaging_method(self, value: dict):
        self._property_changed('leg_one_averaging_method')
        self.__leg_one_averaging_method = value        

    @property
    def option_type(self) -> dict:
        return self.__option_type

    @option_type.setter
    def option_type(self, value: dict):
        self._property_changed('option_type')
        self.__option_type = value        

    @property
    def portfolio_assets(self) -> dict:
        return self.__portfolio_assets

    @portfolio_assets.setter
    def portfolio_assets(self, value: dict):
        self._property_changed('portfolio_assets')
        self.__portfolio_assets = value        

    @property
    def tcm_cost_horizon3_hour(self) -> dict:
        return self.__tcm_cost_horizon3_hour

    @tcm_cost_horizon3_hour.setter
    def tcm_cost_horizon3_hour(self, value: dict):
        self._property_changed('tcm_cost_horizon3_hour')
        self.__tcm_cost_horizon3_hour = value        

    @property
    def number_covered(self) -> dict:
        return self.__number_covered

    @number_covered.setter
    def number_covered(self, value: dict):
        self._property_changed('number_covered')
        self.__number_covered = value        

    @property
    def credit_limit(self) -> dict:
        return self.__credit_limit

    @credit_limit.setter
    def credit_limit(self, value: dict):
        self._property_changed('credit_limit')
        self.__credit_limit = value        

    @property
    def number_of_positions(self) -> dict:
        return self.__number_of_positions

    @number_of_positions.setter
    def number_of_positions(self, value: dict):
        self._property_changed('number_of_positions')
        self.__number_of_positions = value        

    @property
    def effective_tenor(self) -> dict:
        return self.__effective_tenor

    @effective_tenor.setter
    def effective_tenor(self, value: dict):
        self._property_changed('effective_tenor')
        self.__effective_tenor = value        

    @property
    def open_unadjusted(self) -> dict:
        return self.__open_unadjusted

    @open_unadjusted.setter
    def open_unadjusted(self, value: dict):
        self._property_changed('open_unadjusted')
        self.__open_unadjusted = value        

    @property
    def ask_price(self) -> dict:
        return self.__ask_price

    @ask_price.setter
    def ask_price(self, value: dict):
        self._property_changed('ask_price')
        self.__ask_price = value        

    @property
    def event_id(self) -> dict:
        return self.__event_id

    @event_id.setter
    def event_id(self, value: dict):
        self._property_changed('event_id')
        self.__event_id = value        

    @property
    def sectors(self) -> dict:
        return self.__sectors

    @sectors.setter
    def sectors(self, value: dict):
        self._property_changed('sectors')
        self.__sectors = value        

    @property
    def std30_days_subsidized_yield(self) -> dict:
        return self.__std30_days_subsidized_yield

    @std30_days_subsidized_yield.setter
    def std30_days_subsidized_yield(self, value: dict):
        self._property_changed('std30_days_subsidized_yield')
        self.__std30_days_subsidized_yield = value        

    @property
    def annualized_tracking_error(self) -> dict:
        return self.__annualized_tracking_error

    @annualized_tracking_error.setter
    def annualized_tracking_error(self, value: dict):
        self._property_changed('annualized_tracking_error')
        self.__annualized_tracking_error = value        

    @property
    def additional_price_notation_type(self) -> dict:
        return self.__additional_price_notation_type

    @additional_price_notation_type.setter
    def additional_price_notation_type(self, value: dict):
        self._property_changed('additional_price_notation_type')
        self.__additional_price_notation_type = value        

    @property
    def vol_swap(self) -> dict:
        return self.__vol_swap

    @vol_swap.setter
    def vol_swap(self, value: dict):
        self._property_changed('vol_swap')
        self.__vol_swap = value        

    @property
    def real_fci(self) -> dict:
        return self.__real_fci

    @real_fci.setter
    def real_fci(self, value: dict):
        self._property_changed('real_fci')
        self.__real_fci = value        

    @property
    def annualized_risk(self) -> dict:
        return self.__annualized_risk

    @annualized_risk.setter
    def annualized_risk(self, value: dict):
        self._property_changed('annualized_risk')
        self.__annualized_risk = value        

    @property
    def block_trades_and_large_notional_off_facility_swaps(self) -> dict:
        return self.__block_trades_and_large_notional_off_facility_swaps

    @block_trades_and_large_notional_off_facility_swaps.setter
    def block_trades_and_large_notional_off_facility_swaps(self, value: dict):
        self._property_changed('block_trades_and_large_notional_off_facility_swaps')
        self.__block_trades_and_large_notional_off_facility_swaps = value        

    @property
    def leg_one_fixed_payment_currency(self) -> dict:
        return self.__leg_one_fixed_payment_currency

    @leg_one_fixed_payment_currency.setter
    def leg_one_fixed_payment_currency(self, value: dict):
        self._property_changed('leg_one_fixed_payment_currency')
        self.__leg_one_fixed_payment_currency = value        

    @property
    def gross_exposure(self) -> dict:
        return self.__gross_exposure

    @gross_exposure.setter
    def gross_exposure(self, value: dict):
        self._property_changed('gross_exposure')
        self.__gross_exposure = value        

    @property
    def payment_frequency_leg1(self) -> dict:
        return self.__payment_frequency_leg1

    @payment_frequency_leg1.setter
    def payment_frequency_leg1(self, value: dict):
        self._property_changed('payment_frequency_leg1')
        self.__payment_frequency_leg1 = value        

    @property
    def payment_frequency_leg2(self) -> dict:
        return self.__payment_frequency_leg2

    @payment_frequency_leg2.setter
    def payment_frequency_leg2(self, value: dict):
        self._property_changed('payment_frequency_leg2')
        self.__payment_frequency_leg2 = value        

    @property
    def volume_composite(self) -> dict:
        return self.__volume_composite

    @volume_composite.setter
    def volume_composite(self, value: dict):
        self._property_changed('volume_composite')
        self.__volume_composite = value        

    @property
    def volume(self) -> dict:
        return self.__volume

    @volume.setter
    def volume(self, value: dict):
        self._property_changed('volume')
        self.__volume = value        

    @property
    def adv(self) -> dict:
        return self.__adv

    @adv.setter
    def adv(self, value: dict):
        self._property_changed('adv')
        self.__adv = value        

    @property
    def external(self) -> dict:
        return self.__external

    @external.setter
    def external(self, value: dict):
        self._property_changed('external')
        self.__external = value        

    @property
    def short_conviction_medium(self) -> dict:
        return self.__short_conviction_medium

    @short_conviction_medium.setter
    def short_conviction_medium(self, value: dict):
        self._property_changed('short_conviction_medium')
        self.__short_conviction_medium = value        

    @property
    def exchange(self) -> dict:
        return self.__exchange

    @exchange.setter
    def exchange(self, value: dict):
        self._property_changed('exchange')
        self.__exchange = value        

    @property
    def trade_price(self) -> dict:
        return self.__trade_price

    @trade_price.setter
    def trade_price(self, value: dict):
        self._property_changed('trade_price')
        self.__trade_price = value        

    @property
    def cleared(self) -> dict:
        return self.__cleared

    @cleared.setter
    def cleared(self, value: dict):
        self._property_changed('cleared')
        self.__cleared = value        

    @property
    def es_policy_score(self) -> dict:
        return self.__es_policy_score

    @es_policy_score.setter
    def es_policy_score(self, value: dict):
        self._property_changed('es_policy_score')
        self.__es_policy_score = value        

    @property
    def prime_id_numeric(self) -> dict:
        return self.__prime_id_numeric

    @prime_id_numeric.setter
    def prime_id_numeric(self, value: dict):
        self._property_changed('prime_id_numeric')
        self.__prime_id_numeric = value        

    @property
    def cid(self) -> dict:
        return self.__cid

    @cid.setter
    def cid(self, value: dict):
        self._property_changed('cid')
        self.__cid = value        

    @property
    def leg_one_index(self) -> dict:
        return self.__leg_one_index

    @leg_one_index.setter
    def leg_one_index(self, value: dict):
        self._property_changed('leg_one_index')
        self.__leg_one_index = value        

    @property
    def on_loan_percentage(self) -> dict:
        return self.__on_loan_percentage

    @on_loan_percentage.setter
    def on_loan_percentage(self, value: dict):
        self._property_changed('on_loan_percentage')
        self.__on_loan_percentage = value        

    @property
    def bid_high(self) -> dict:
        return self.__bid_high

    @bid_high.setter
    def bid_high(self, value: dict):
        self._property_changed('bid_high')
        self.__bid_high = value        

    @property
    def fair_variance(self) -> dict:
        return self.__fair_variance

    @fair_variance.setter
    def fair_variance(self, value: dict):
        self._property_changed('fair_variance')
        self.__fair_variance = value        

    @property
    def hit_rate_wtd(self) -> dict:
        return self.__hit_rate_wtd

    @hit_rate_wtd.setter
    def hit_rate_wtd(self, value: dict):
        self._property_changed('hit_rate_wtd')
        self.__hit_rate_wtd = value        

    @property
    def bos_in_bps_description(self) -> dict:
        return self.__bos_in_bps_description

    @bos_in_bps_description.setter
    def bos_in_bps_description(self, value: dict):
        self._property_changed('bos_in_bps_description')
        self.__bos_in_bps_description = value        

    @property
    def low_price(self) -> dict:
        return self.__low_price

    @low_price.setter
    def low_price(self, value: dict):
        self._property_changed('low_price')
        self.__low_price = value        

    @property
    def realized_volatility(self) -> dict:
        return self.__realized_volatility

    @realized_volatility.setter
    def realized_volatility(self, value: dict):
        self._property_changed('realized_volatility')
        self.__realized_volatility = value        

    @property
    def adv22_day_pct(self) -> dict:
        return self.__adv22_day_pct

    @adv22_day_pct.setter
    def adv22_day_pct(self, value: dict):
        self._property_changed('adv22_day_pct')
        self.__adv22_day_pct = value        

    @property
    def clone_parent_id(self) -> dict:
        return self.__clone_parent_id

    @clone_parent_id.setter
    def clone_parent_id(self, value: dict):
        self._property_changed('clone_parent_id')
        self.__clone_parent_id = value        

    @property
    def price_range_in_ticks_label(self) -> tuple:
        return self.__price_range_in_ticks_label

    @price_range_in_ticks_label.setter
    def price_range_in_ticks_label(self, value: tuple):
        self._property_changed('price_range_in_ticks_label')
        self.__price_range_in_ticks_label = value        

    @property
    def ticker(self) -> dict:
        return self.__ticker

    @ticker.setter
    def ticker(self, value: dict):
        self._property_changed('ticker')
        self.__ticker = value        

    @property
    def tcm_cost_horizon1_day(self) -> dict:
        return self.__tcm_cost_horizon1_day

    @tcm_cost_horizon1_day.setter
    def tcm_cost_horizon1_day(self, value: dict):
        self._property_changed('tcm_cost_horizon1_day')
        self.__tcm_cost_horizon1_day = value        

    @property
    def approval(self) -> dict:
        return self.__approval

    @approval.setter
    def approval(self, value: dict):
        self._property_changed('approval')
        self.__approval = value        

    @property
    def file_location(self) -> dict:
        return self.__file_location

    @file_location.setter
    def file_location(self, value: dict):
        self._property_changed('file_location')
        self.__file_location = value        

    @property
    def sts_rates_country(self) -> dict:
        return self.__sts_rates_country

    @sts_rates_country.setter
    def sts_rates_country(self, value: dict):
        self._property_changed('sts_rates_country')
        self.__sts_rates_country = value        

    @property
    def leg_two_payment_type(self) -> dict:
        return self.__leg_two_payment_type

    @leg_two_payment_type.setter
    def leg_two_payment_type(self, value: dict):
        self._property_changed('leg_two_payment_type')
        self.__leg_two_payment_type = value        

    @property
    def horizon(self) -> dict:
        return self.__horizon

    @horizon.setter
    def horizon(self, value: dict):
        self._property_changed('horizon')
        self.__horizon = value        

    @property
    def day_count_convention_leg1(self) -> dict:
        return self.__day_count_convention_leg1

    @day_count_convention_leg1.setter
    def day_count_convention_leg1(self, value: dict):
        self._property_changed('day_count_convention_leg1')
        self.__day_count_convention_leg1 = value        

    @property
    def source_value_forecast(self) -> dict:
        return self.__source_value_forecast

    @source_value_forecast.setter
    def source_value_forecast(self, value: dict):
        self._property_changed('source_value_forecast')
        self.__source_value_forecast = value        

    @property
    def short_conviction_large(self) -> dict:
        return self.__short_conviction_large

    @short_conviction_large.setter
    def short_conviction_large(self, value: dict):
        self._property_changed('short_conviction_large')
        self.__short_conviction_large = value        

    @property
    def day_count_convention_leg2(self) -> dict:
        return self.__day_count_convention_leg2

    @day_count_convention_leg2.setter
    def day_count_convention_leg2(self, value: dict):
        self._property_changed('day_count_convention_leg2')
        self.__day_count_convention_leg2 = value        

    @property
    def counter_party_status(self) -> dict:
        return self.__counter_party_status

    @counter_party_status.setter
    def counter_party_status(self, value: dict):
        self._property_changed('counter_party_status')
        self.__counter_party_status = value        

    @property
    def composite22_day_adv(self) -> dict:
        return self.__composite22_day_adv

    @composite22_day_adv.setter
    def composite22_day_adv(self, value: dict):
        self._property_changed('composite22_day_adv')
        self.__composite22_day_adv = value        

    @property
    def dollar_excess_return(self) -> dict:
        return self.__dollar_excess_return

    @dollar_excess_return.setter
    def dollar_excess_return(self, value: dict):
        self._property_changed('dollar_excess_return')
        self.__dollar_excess_return = value        

    @property
    def gsn(self) -> dict:
        return self.__gsn

    @gsn.setter
    def gsn(self, value: dict):
        self._property_changed('gsn')
        self.__gsn = value        

    @property
    def gss(self) -> dict:
        return self.__gss

    @gss.setter
    def gss(self, value: dict):
        self._property_changed('gss')
        self.__gss = value        

    @property
    def percent_of_mediandv1m(self) -> dict:
        return self.__percent_of_mediandv1m

    @percent_of_mediandv1m.setter
    def percent_of_mediandv1m(self, value: dict):
        self._property_changed('percent_of_mediandv1m')
        self.__percent_of_mediandv1m = value        

    @property
    def lendables(self) -> dict:
        return self.__lendables

    @lendables.setter
    def lendables(self, value: dict):
        self._property_changed('lendables')
        self.__lendables = value        

    @property
    def loan_spread_required(self) -> dict:
        return self.__loan_spread_required

    @loan_spread_required.setter
    def loan_spread_required(self, value: dict):
        self._property_changed('loan_spread_required')
        self.__loan_spread_required = value        

    @property
    def asset_class(self) -> dict:
        return self.__asset_class

    @asset_class.setter
    def asset_class(self, value: dict):
        self._property_changed('asset_class')
        self.__asset_class = value        

    @property
    def sovereign_spread_contribution(self) -> dict:
        return self.__sovereign_spread_contribution

    @sovereign_spread_contribution.setter
    def sovereign_spread_contribution(self, value: dict):
        self._property_changed('sovereign_spread_contribution')
        self.__sovereign_spread_contribution = value        

    @property
    def bos_in_ticks_label(self) -> tuple:
        return self.__bos_in_ticks_label

    @bos_in_ticks_label.setter
    def bos_in_ticks_label(self, value: tuple):
        self._property_changed('bos_in_ticks_label')
        self.__bos_in_ticks_label = value        

    @property
    def ric(self) -> dict:
        return self.__ric

    @ric.setter
    def ric(self, value: dict):
        self._property_changed('ric')
        self.__ric = value        

    @property
    def position_source_id(self) -> dict:
        return self.__position_source_id

    @position_source_id.setter
    def position_source_id(self, value: dict):
        self._property_changed('position_source_id')
        self.__position_source_id = value        

    @property
    def rate_type(self) -> dict:
        return self.__rate_type

    @rate_type.setter
    def rate_type(self, value: dict):
        self._property_changed('rate_type')
        self.__rate_type = value        

    @property
    def gs_sustain_region(self) -> dict:
        return self.__gs_sustain_region

    @gs_sustain_region.setter
    def gs_sustain_region(self, value: dict):
        self._property_changed('gs_sustain_region')
        self.__gs_sustain_region = value        

    @property
    def deployment_id(self) -> dict:
        return self.__deployment_id

    @deployment_id.setter
    def deployment_id(self, value: dict):
        self._property_changed('deployment_id')
        self.__deployment_id = value        

    @property
    def loan_status(self) -> dict:
        return self.__loan_status

    @loan_status.setter
    def loan_status(self, value: dict):
        self._property_changed('loan_status')
        self.__loan_status = value        

    @property
    def short_weight(self) -> dict:
        return self.__short_weight

    @short_weight.setter
    def short_weight(self, value: dict):
        self._property_changed('short_weight')
        self.__short_weight = value        

    @property
    def geography_id(self) -> dict:
        return self.__geography_id

    @geography_id.setter
    def geography_id(self, value: dict):
        self._property_changed('geography_id')
        self.__geography_id = value        

    @property
    def loan_rebate(self) -> dict:
        return self.__loan_rebate

    @loan_rebate.setter
    def loan_rebate(self, value: dict):
        self._property_changed('loan_rebate')
        self.__loan_rebate = value        

    @property
    def period(self) -> dict:
        return self.__period

    @period.setter
    def period(self, value: dict):
        self._property_changed('period')
        self.__period = value        

    @property
    def index_create_source(self) -> dict:
        return self.__index_create_source

    @index_create_source.setter
    def index_create_source(self, value: dict):
        self._property_changed('index_create_source')
        self.__index_create_source = value        

    @property
    def fiscal_quarter(self) -> dict:
        return self.__fiscal_quarter

    @fiscal_quarter.setter
    def fiscal_quarter(self, value: dict):
        self._property_changed('fiscal_quarter')
        self.__fiscal_quarter = value        

    @property
    def version_string(self) -> dict:
        return self.__version_string

    @version_string.setter
    def version_string(self, value: dict):
        self._property_changed('version_string')
        self.__version_string = value        

    @property
    def real_twi_contribution(self) -> dict:
        return self.__real_twi_contribution

    @real_twi_contribution.setter
    def real_twi_contribution(self, value: dict):
        self._property_changed('real_twi_contribution')
        self.__real_twi_contribution = value        

    @property
    def market_impact(self) -> dict:
        return self.__market_impact

    @market_impact.setter
    def market_impact(self, value: dict):
        self._property_changed('market_impact')
        self.__market_impact = value        

    @property
    def event_type(self) -> dict:
        return self.__event_type

    @event_type.setter
    def event_type(self, value: dict):
        self._property_changed('event_type')
        self.__event_type = value        

    @property
    def mkt_asset(self) -> dict:
        return self.__mkt_asset

    @mkt_asset.setter
    def mkt_asset(self, value: dict):
        self._property_changed('mkt_asset')
        self.__mkt_asset = value        

    @property
    def asset_count_long(self) -> dict:
        return self.__asset_count_long

    @asset_count_long.setter
    def asset_count_long(self, value: dict):
        self._property_changed('asset_count_long')
        self.__asset_count_long = value        

    @property
    def spot(self) -> dict:
        return self.__spot

    @spot.setter
    def spot(self, value: dict):
        self._property_changed('spot')
        self.__spot = value        

    @property
    def last_updated_message(self) -> dict:
        return self.__last_updated_message

    @last_updated_message.setter
    def last_updated_message(self, value: dict):
        self._property_changed('last_updated_message')
        self.__last_updated_message = value        

    @property
    def underlying_asset_leg2(self) -> dict:
        return self.__underlying_asset_leg2

    @underlying_asset_leg2.setter
    def underlying_asset_leg2(self, value: dict):
        self._property_changed('underlying_asset_leg2')
        self.__underlying_asset_leg2 = value        

    @property
    def loan_value(self) -> dict:
        return self.__loan_value

    @loan_value.setter
    def loan_value(self, value: dict):
        self._property_changed('loan_value')
        self.__loan_value = value        

    @property
    def underlying_asset_leg1(self) -> dict:
        return self.__underlying_asset_leg1

    @underlying_asset_leg1.setter
    def underlying_asset_leg1(self, value: dict):
        self._property_changed('underlying_asset_leg1')
        self.__underlying_asset_leg1 = value        

    @property
    def swap_spread(self) -> dict:
        return self.__swap_spread

    @swap_spread.setter
    def swap_spread(self, value: dict):
        self._property_changed('swap_spread')
        self.__swap_spread = value        

    @property
    def trading_restriction(self) -> dict:
        return self.__trading_restriction

    @trading_restriction.setter
    def trading_restriction(self, value: dict):
        self._property_changed('trading_restriction')
        self.__trading_restriction = value        

    @property
    def asset_parameters_pay_or_receive(self) -> dict:
        return self.__asset_parameters_pay_or_receive

    @asset_parameters_pay_or_receive.setter
    def asset_parameters_pay_or_receive(self, value: dict):
        self._property_changed('asset_parameters_pay_or_receive')
        self.__asset_parameters_pay_or_receive = value        

    @property
    def price_spot_entry_unit(self) -> dict:
        return self.__price_spot_entry_unit

    @price_spot_entry_unit.setter
    def price_spot_entry_unit(self, value: dict):
        self._property_changed('price_spot_entry_unit')
        self.__price_spot_entry_unit = value        

    @property
    def total_return_price(self) -> dict:
        return self.__total_return_price

    @total_return_price.setter
    def total_return_price(self, value: dict):
        self._property_changed('total_return_price')
        self.__total_return_price = value        

    @property
    def weighted_percent_in_model(self) -> dict:
        return self.__weighted_percent_in_model

    @weighted_percent_in_model.setter
    def weighted_percent_in_model(self, value: dict):
        self._property_changed('weighted_percent_in_model')
        self.__weighted_percent_in_model = value        

    @property
    def city(self) -> dict:
        return self.__city

    @city.setter
    def city(self, value: dict):
        self._property_changed('city')
        self.__city = value        

    @property
    def election_period(self) -> dict:
        return self.__election_period

    @election_period.setter
    def election_period(self, value: dict):
        self._property_changed('election_period')
        self.__election_period = value        

    @property
    def funding_ask_price(self) -> dict:
        return self.__funding_ask_price

    @funding_ask_price.setter
    def funding_ask_price(self, value: dict):
        self._property_changed('funding_ask_price')
        self.__funding_ask_price = value        

    @property
    def historical_beta(self) -> dict:
        return self.__historical_beta

    @historical_beta.setter
    def historical_beta(self, value: dict):
        self._property_changed('historical_beta')
        self.__historical_beta = value        

    @property
    def dissemination_id(self) -> dict:
        return self.__dissemination_id

    @dissemination_id.setter
    def dissemination_id(self, value: dict):
        self._property_changed('dissemination_id')
        self.__dissemination_id = value        

    @property
    def bond_risk_premium_index(self) -> dict:
        return self.__bond_risk_premium_index

    @bond_risk_premium_index.setter
    def bond_risk_premium_index(self, value: dict):
        self._property_changed('bond_risk_premium_index')
        self.__bond_risk_premium_index = value        

    @property
    def leg_two_fixed_payment(self) -> dict:
        return self.__leg_two_fixed_payment

    @leg_two_fixed_payment.setter
    def leg_two_fixed_payment(self, value: dict):
        self._property_changed('leg_two_fixed_payment')
        self.__leg_two_fixed_payment = value        

    @property
    def commodity_forecast(self) -> dict:
        return self.__commodity_forecast

    @commodity_forecast.setter
    def commodity_forecast(self, value: dict):
        self._property_changed('commodity_forecast')
        self.__commodity_forecast = value        

    @property
    def hit_rate_ytd(self) -> dict:
        return self.__hit_rate_ytd

    @hit_rate_ytd.setter
    def hit_rate_ytd(self, value: dict):
        self._property_changed('hit_rate_ytd')
        self.__hit_rate_ytd = value        

    @property
    def valid(self) -> dict:
        return self.__valid

    @valid.setter
    def valid(self, value: dict):
        self._property_changed('valid')
        self.__valid = value        

    @property
    def sts_commodity(self) -> dict:
        return self.__sts_commodity

    @sts_commodity.setter
    def sts_commodity(self, value: dict):
        self._property_changed('sts_commodity')
        self.__sts_commodity = value        

    @property
    def indication_of_end_user_exception(self) -> dict:
        return self.__indication_of_end_user_exception

    @indication_of_end_user_exception.setter
    def indication_of_end_user_exception(self, value: dict):
        self._property_changed('indication_of_end_user_exception')
        self.__indication_of_end_user_exception = value        

    @property
    def es_score(self) -> dict:
        return self.__es_score

    @es_score.setter
    def es_score(self, value: dict):
        self._property_changed('es_score')
        self.__es_score = value        

    @property
    def price_range_in_ticks(self) -> dict:
        return self.__price_range_in_ticks

    @price_range_in_ticks.setter
    def price_range_in_ticks(self, value: dict):
        self._property_changed('price_range_in_ticks')
        self.__price_range_in_ticks = value        

    @property
    def expense_ratio_gross_bps(self) -> dict:
        return self.__expense_ratio_gross_bps

    @expense_ratio_gross_bps.setter
    def expense_ratio_gross_bps(self, value: dict):
        self._property_changed('expense_ratio_gross_bps')
        self.__expense_ratio_gross_bps = value        

    @property
    def pct_change(self) -> dict:
        return self.__pct_change

    @pct_change.setter
    def pct_change(self, value: dict):
        self._property_changed('pct_change')
        self.__pct_change = value        

    @property
    def number_of_rolls(self) -> dict:
        return self.__number_of_rolls

    @number_of_rolls.setter
    def number_of_rolls(self, value: dict):
        self._property_changed('number_of_rolls')
        self.__number_of_rolls = value        

    @property
    def agent_lender_fee(self) -> dict:
        return self.__agent_lender_fee

    @agent_lender_fee.setter
    def agent_lender_fee(self, value: dict):
        self._property_changed('agent_lender_fee')
        self.__agent_lender_fee = value        

    @property
    def bbid(self) -> dict:
        return self.__bbid

    @bbid.setter
    def bbid(self, value: dict):
        self._property_changed('bbid')
        self.__bbid = value        

    @property
    def option_strike_price(self) -> dict:
        return self.__option_strike_price

    @option_strike_price.setter
    def option_strike_price(self, value: dict):
        self._property_changed('option_strike_price')
        self.__option_strike_price = value        

    @property
    def price_type_leg3(self) -> dict:
        return self.__price_type_leg3

    @price_type_leg3.setter
    def price_type_leg3(self, value: dict):
        self._property_changed('price_type_leg3')
        self.__price_type_leg3 = value        

    @property
    def arrival_mid_normalized(self) -> dict:
        return self.__arrival_mid_normalized

    @arrival_mid_normalized.setter
    def arrival_mid_normalized(self, value: dict):
        self._property_changed('arrival_mid_normalized')
        self.__arrival_mid_normalized = value        

    @property
    def underlying_asset2(self) -> dict:
        return self.__underlying_asset2

    @underlying_asset2.setter
    def underlying_asset2(self, value: dict):
        self._property_changed('underlying_asset2')
        self.__underlying_asset2 = value        

    @property
    def underlying_asset1(self) -> dict:
        return self.__underlying_asset1

    @underlying_asset1.setter
    def underlying_asset1(self, value: dict):
        self._property_changed('underlying_asset1')
        self.__underlying_asset1 = value        

    @property
    def rounded_notional_amount_leg1(self) -> dict:
        return self.__rounded_notional_amount_leg1

    @rounded_notional_amount_leg1.setter
    def rounded_notional_amount_leg1(self, value: dict):
        self._property_changed('rounded_notional_amount_leg1')
        self.__rounded_notional_amount_leg1 = value        

    @property
    def rounded_notional_amount_leg2(self) -> dict:
        return self.__rounded_notional_amount_leg2

    @rounded_notional_amount_leg2.setter
    def rounded_notional_amount_leg2(self, value: dict):
        self._property_changed('rounded_notional_amount_leg2')
        self.__rounded_notional_amount_leg2 = value        

    @property
    def capped(self) -> dict:
        return self.__capped

    @capped.setter
    def capped(self, value: dict):
        self._property_changed('capped')
        self.__capped = value        

    @property
    def rating(self) -> dict:
        return self.__rating

    @rating.setter
    def rating(self, value: dict):
        self._property_changed('rating')
        self.__rating = value        

    @property
    def payment_type_leg1(self) -> dict:
        return self.__payment_type_leg1

    @payment_type_leg1.setter
    def payment_type_leg1(self, value: dict):
        self._property_changed('payment_type_leg1')
        self.__payment_type_leg1 = value        

    @property
    def option_currency(self) -> dict:
        return self.__option_currency

    @option_currency.setter
    def option_currency(self, value: dict):
        self._property_changed('option_currency')
        self.__option_currency = value        

    @property
    def price_leg3(self) -> dict:
        return self.__price_leg3

    @price_leg3.setter
    def price_leg3(self, value: dict):
        self._property_changed('price_leg3')
        self.__price_leg3 = value        

    @property
    def price_leg2(self) -> dict:
        return self.__price_leg2

    @price_leg2.setter
    def price_leg2(self, value: dict):
        self._property_changed('price_leg2')
        self.__price_leg2 = value        

    @property
    def volatility(self) -> dict:
        return self.__volatility

    @volatility.setter
    def volatility(self, value: dict):
        self._property_changed('volatility')
        self.__volatility = value        

    @property
    def price_leg1(self) -> dict:
        return self.__price_leg1

    @price_leg1.setter
    def price_leg1(self, value: dict):
        self._property_changed('price_leg1')
        self.__price_leg1 = value        

    @property
    def price_type_leg2(self) -> dict:
        return self.__price_type_leg2

    @price_type_leg2.setter
    def price_type_leg2(self, value: dict):
        self._property_changed('price_type_leg2')
        self.__price_type_leg2 = value        

    @property
    def legal_entity(self) -> dict:
        return self.__legal_entity

    @legal_entity.setter
    def legal_entity(self, value: dict):
        self._property_changed('legal_entity')
        self.__legal_entity = value        

    @property
    def performance_fee(self) -> dict:
        return self.__performance_fee

    @performance_fee.setter
    def performance_fee(self, value: dict):
        self._property_changed('performance_fee')
        self.__performance_fee = value        

    @property
    def price_type_leg1(self) -> dict:
        return self.__price_type_leg1

    @price_type_leg1.setter
    def price_type_leg1(self, value: dict):
        self._property_changed('price_type_leg1')
        self.__price_type_leg1 = value        

    @property
    def payment_type_leg2(self) -> dict:
        return self.__payment_type_leg2

    @payment_type_leg2.setter
    def payment_type_leg2(self, value: dict):
        self._property_changed('payment_type_leg2')
        self.__payment_type_leg2 = value        

    @property
    def type_leg1(self) -> dict:
        return self.__type_leg1

    @type_leg1.setter
    def type_leg1(self, value: dict):
        self._property_changed('type_leg1')
        self.__type_leg1 = value        

    @property
    def underlying_asset_ids(self) -> dict:
        return self.__underlying_asset_ids

    @underlying_asset_ids.setter
    def underlying_asset_ids(self, value: dict):
        self._property_changed('underlying_asset_ids')
        self.__underlying_asset_ids = value        

    @property
    def type_leg2(self) -> dict:
        return self.__type_leg2

    @type_leg2.setter
    def type_leg2(self, value: dict):
        self._property_changed('type_leg2')
        self.__type_leg2 = value        

    @property
    def queue_in_lots_label(self) -> tuple:
        return self.__queue_in_lots_label

    @queue_in_lots_label.setter
    def queue_in_lots_label(self, value: tuple):
        self._property_changed('queue_in_lots_label')
        self.__queue_in_lots_label = value        

    @property
    def adv10_day_pct(self) -> dict:
        return self.__adv10_day_pct

    @adv10_day_pct.setter
    def adv10_day_pct(self, value: dict):
        self._property_changed('adv10_day_pct')
        self.__adv10_day_pct = value        

    @property
    def long_conviction_medium(self) -> dict:
        return self.__long_conviction_medium

    @long_conviction_medium.setter
    def long_conviction_medium(self, value: dict):
        self._property_changed('long_conviction_medium')
        self.__long_conviction_medium = value        

    @property
    def annual_risk(self) -> dict:
        return self.__annual_risk

    @annual_risk.setter
    def annual_risk(self, value: dict):
        self._property_changed('annual_risk')
        self.__annual_risk = value        

    @property
    def eti(self) -> dict:
        return self.__eti

    @eti.setter
    def eti(self, value: dict):
        self._property_changed('eti')
        self.__eti = value        

    @property
    def daily_tracking_error(self) -> dict:
        return self.__daily_tracking_error

    @daily_tracking_error.setter
    def daily_tracking_error(self, value: dict):
        self._property_changed('daily_tracking_error')
        self.__daily_tracking_error = value        

    @property
    def leg_two_index(self) -> dict:
        return self.__leg_two_index

    @leg_two_index.setter
    def leg_two_index(self, value: dict):
        self._property_changed('leg_two_index')
        self.__leg_two_index = value        

    @property
    def market_buffer(self) -> dict:
        return self.__market_buffer

    @market_buffer.setter
    def market_buffer(self, value: dict):
        self._property_changed('market_buffer')
        self.__market_buffer = value        

    @property
    def market_cap(self) -> dict:
        return self.__market_cap

    @market_cap.setter
    def market_cap(self, value: dict):
        self._property_changed('market_cap')
        self.__market_cap = value        

    @property
    def oe_id(self) -> dict:
        return self.__oe_id

    @oe_id.setter
    def oe_id(self, value: dict):
        self._property_changed('oe_id')
        self.__oe_id = value        

    @property
    def cluster_region(self) -> tuple:
        return self.__cluster_region

    @cluster_region.setter
    def cluster_region(self, value: tuple):
        self._property_changed('cluster_region')
        self.__cluster_region = value        

    @property
    def bbid_equivalent(self) -> dict:
        return self.__bbid_equivalent

    @bbid_equivalent.setter
    def bbid_equivalent(self, value: dict):
        self._property_changed('bbid_equivalent')
        self.__bbid_equivalent = value        

    @property
    def valoren(self) -> dict:
        return self.__valoren

    @valoren.setter
    def valoren(self, value: dict):
        self._property_changed('valoren')
        self.__valoren = value        

    @property
    def basis(self) -> dict:
        return self.__basis

    @basis.setter
    def basis(self, value: dict):
        self._property_changed('basis')
        self.__basis = value        

    @property
    def investment_rate_trend(self) -> dict:
        return self.__investment_rate_trend

    @investment_rate_trend.setter
    def investment_rate_trend(self, value: dict):
        self._property_changed('investment_rate_trend')
        self.__investment_rate_trend = value        

    @property
    def ext_mkt_class(self) -> dict:
        return self.__ext_mkt_class

    @ext_mkt_class.setter
    def ext_mkt_class(self, value: dict):
        self._property_changed('ext_mkt_class')
        self.__ext_mkt_class = value        

    @property
    def price_currency(self) -> dict:
        return self.__price_currency

    @price_currency.setter
    def price_currency(self, value: dict):
        self._property_changed('price_currency')
        self.__price_currency = value        

    @property
    def hedge_id(self) -> dict:
        return self.__hedge_id

    @hedge_id.setter
    def hedge_id(self, value: dict):
        self._property_changed('hedge_id')
        self.__hedge_id = value        

    @property
    def tcm_cost_horizon8_day(self) -> dict:
        return self.__tcm_cost_horizon8_day

    @tcm_cost_horizon8_day.setter
    def tcm_cost_horizon8_day(self, value: dict):
        self._property_changed('tcm_cost_horizon8_day')
        self.__tcm_cost_horizon8_day = value        

    @property
    def residual_variance(self) -> dict:
        return self.__residual_variance

    @residual_variance.setter
    def residual_variance(self, value: dict):
        self._property_changed('residual_variance')
        self.__residual_variance = value        

    @property
    def supra_strategy(self) -> dict:
        return self.__supra_strategy

    @supra_strategy.setter
    def supra_strategy(self, value: dict):
        self._property_changed('supra_strategy')
        self.__supra_strategy = value        

    @property
    def restrict_internal_derived_data(self) -> dict:
        return self.__restrict_internal_derived_data

    @restrict_internal_derived_data.setter
    def restrict_internal_derived_data(self, value: dict):
        self._property_changed('restrict_internal_derived_data')
        self.__restrict_internal_derived_data = value        

    @property
    def day_count_convention(self) -> dict:
        return self.__day_count_convention

    @day_count_convention.setter
    def day_count_convention(self, value: dict):
        self._property_changed('day_count_convention')
        self.__day_count_convention = value        

    @property
    def rounded_notional_amount1(self) -> dict:
        return self.__rounded_notional_amount1

    @rounded_notional_amount1.setter
    def rounded_notional_amount1(self, value: dict):
        self._property_changed('rounded_notional_amount1')
        self.__rounded_notional_amount1 = value        

    @property
    def adv5_day_pct(self) -> dict:
        return self.__adv5_day_pct

    @adv5_day_pct.setter
    def adv5_day_pct(self, value: dict):
        self._property_changed('adv5_day_pct')
        self.__adv5_day_pct = value        

    @property
    def rounded_notional_amount2(self) -> dict:
        return self.__rounded_notional_amount2

    @rounded_notional_amount2.setter
    def rounded_notional_amount2(self, value: dict):
        self._property_changed('rounded_notional_amount2')
        self.__rounded_notional_amount2 = value        

    @property
    def factor_source(self) -> dict:
        return self.__factor_source

    @factor_source.setter
    def factor_source(self, value: dict):
        self._property_changed('factor_source')
        self.__factor_source = value        

    @property
    def lending_sec_type(self) -> dict:
        return self.__lending_sec_type

    @lending_sec_type.setter
    def lending_sec_type(self, value: dict):
        self._property_changed('lending_sec_type')
        self.__lending_sec_type = value        

    @property
    def leverage(self) -> dict:
        return self.__leverage

    @leverage.setter
    def leverage(self, value: dict):
        self._property_changed('leverage')
        self.__leverage = value        

    @property
    def option_family(self) -> dict:
        return self.__option_family

    @option_family.setter
    def option_family(self, value: dict):
        self._property_changed('option_family')
        self.__option_family = value        

    @property
    def price_spot_stop_loss_value(self) -> dict:
        return self.__price_spot_stop_loss_value

    @price_spot_stop_loss_value.setter
    def price_spot_stop_loss_value(self, value: dict):
        self._property_changed('price_spot_stop_loss_value')
        self.__price_spot_stop_loss_value = value        

    @property
    def fwd_points(self) -> dict:
        return self.__fwd_points

    @fwd_points.setter
    def fwd_points(self, value: dict):
        self._property_changed('fwd_points')
        self.__fwd_points = value        

    @property
    def kpi_id(self) -> dict:
        return self.__kpi_id

    @kpi_id.setter
    def kpi_id(self, value: dict):
        self._property_changed('kpi_id')
        self.__kpi_id = value        

    @property
    def relative_return_wtd(self) -> dict:
        return self.__relative_return_wtd

    @relative_return_wtd.setter
    def relative_return_wtd(self, value: dict):
        self._property_changed('relative_return_wtd')
        self.__relative_return_wtd = value        

    @property
    def borrow_cost(self) -> dict:
        return self.__borrow_cost

    @borrow_cost.setter
    def borrow_cost(self, value: dict):
        self._property_changed('borrow_cost')
        self.__borrow_cost = value        

    @property
    def asset_classifications_risk_country_name(self) -> dict:
        return self.__asset_classifications_risk_country_name

    @asset_classifications_risk_country_name.setter
    def asset_classifications_risk_country_name(self, value: dict):
        self._property_changed('asset_classifications_risk_country_name')
        self.__asset_classifications_risk_country_name = value        

    @property
    def risk_model(self) -> dict:
        return self.__risk_model

    @risk_model.setter
    def risk_model(self, value: dict):
        self._property_changed('risk_model')
        self.__risk_model = value        

    @property
    def average_implied_volatility(self) -> dict:
        return self.__average_implied_volatility

    @average_implied_volatility.setter
    def average_implied_volatility(self, value: dict):
        self._property_changed('average_implied_volatility')
        self.__average_implied_volatility = value        

    @property
    def fair_value(self) -> dict:
        return self.__fair_value

    @fair_value.setter
    def fair_value(self, value: dict):
        self._property_changed('fair_value')
        self.__fair_value = value        

    @property
    def adjusted_high_price(self) -> dict:
        return self.__adjusted_high_price

    @adjusted_high_price.setter
    def adjusted_high_price(self, value: dict):
        self._property_changed('adjusted_high_price')
        self.__adjusted_high_price = value        

    @property
    def local_ccy_rate(self) -> dict:
        return self.__local_ccy_rate

    @local_ccy_rate.setter
    def local_ccy_rate(self, value: dict):
        self._property_changed('local_ccy_rate')
        self.__local_ccy_rate = value        

    @property
    def ext_mkt_point1(self) -> dict:
        return self.__ext_mkt_point1

    @ext_mkt_point1.setter
    def ext_mkt_point1(self, value: dict):
        self._property_changed('ext_mkt_point1')
        self.__ext_mkt_point1 = value        

    @property
    def direction(self) -> dict:
        return self.__direction

    @direction.setter
    def direction(self, value: dict):
        self._property_changed('direction')
        self.__direction = value        

    @property
    def ext_mkt_point2(self) -> dict:
        return self.__ext_mkt_point2

    @ext_mkt_point2.setter
    def ext_mkt_point2(self, value: dict):
        self._property_changed('ext_mkt_point2')
        self.__ext_mkt_point2 = value        

    @property
    def sub_region_code(self) -> dict:
        return self.__sub_region_code

    @sub_region_code.setter
    def sub_region_code(self, value: dict):
        self._property_changed('sub_region_code')
        self.__sub_region_code = value        

    @property
    def value_forecast(self) -> dict:
        return self.__value_forecast

    @value_forecast.setter
    def value_forecast(self, value: dict):
        self._property_changed('value_forecast')
        self.__value_forecast = value        

    @property
    def execution_venue(self) -> dict:
        return self.__execution_venue

    @execution_venue.setter
    def execution_venue(self, value: dict):
        self._property_changed('execution_venue')
        self.__execution_venue = value        

    @property
    def position_source_type(self) -> dict:
        return self.__position_source_type

    @position_source_type.setter
    def position_source_type(self, value: dict):
        self._property_changed('position_source_type')
        self.__position_source_type = value        

    @property
    def approve_rebalance(self) -> dict:
        return self.__approve_rebalance

    @approve_rebalance.setter
    def approve_rebalance(self, value: dict):
        self._property_changed('approve_rebalance')
        self.__approve_rebalance = value        

    @property
    def adjusted_close_price(self) -> dict:
        return self.__adjusted_close_price

    @adjusted_close_price.setter
    def adjusted_close_price(self, value: dict):
        self._property_changed('adjusted_close_price')
        self.__adjusted_close_price = value        

    @property
    def lms_id(self) -> dict:
        return self.__lms_id

    @lms_id.setter
    def lms_id(self, value: dict):
        self._property_changed('lms_id')
        self.__lms_id = value        

    @property
    def rebate_rate(self) -> dict:
        return self.__rebate_rate

    @rebate_rate.setter
    def rebate_rate(self, value: dict):
        self._property_changed('rebate_rate')
        self.__rebate_rate = value        

    @property
    def participation_rate(self) -> dict:
        return self.__participation_rate

    @participation_rate.setter
    def participation_rate(self, value: dict):
        self._property_changed('participation_rate')
        self.__participation_rate = value        

    @property
    def obfr(self) -> dict:
        return self.__obfr

    @obfr.setter
    def obfr(self, value: dict):
        self._property_changed('obfr')
        self.__obfr = value        

    @property
    def option_lock_period(self) -> dict:
        return self.__option_lock_period

    @option_lock_period.setter
    def option_lock_period(self, value: dict):
        self._property_changed('option_lock_period')
        self.__option_lock_period = value        

    @property
    def strike_relative(self) -> dict:
        return self.__strike_relative

    @strike_relative.setter
    def strike_relative(self, value: dict):
        self._property_changed('strike_relative')
        self.__strike_relative = value        

    @property
    def es_momentum_percentile(self) -> dict:
        return self.__es_momentum_percentile

    @es_momentum_percentile.setter
    def es_momentum_percentile(self, value: dict):
        self._property_changed('es_momentum_percentile')
        self.__es_momentum_percentile = value        

    @property
    def price_notation(self) -> dict:
        return self.__price_notation

    @price_notation.setter
    def price_notation(self, value: dict):
        self._property_changed('price_notation')
        self.__price_notation = value        

    @property
    def strategy(self) -> dict:
        return self.__strategy

    @strategy.setter
    def strategy(self, value: dict):
        self._property_changed('strategy')
        self.__strategy = value        

    @property
    def position_type(self) -> dict:
        return self.__position_type

    @position_type.setter
    def position_type(self, value: dict):
        self._property_changed('position_type')
        self.__position_type = value        

    @property
    def lender_income(self) -> dict:
        return self.__lender_income

    @lender_income.setter
    def lender_income(self, value: dict):
        self._property_changed('lender_income')
        self.__lender_income = value        

    @property
    def sub_asset_class(self) -> dict:
        return self.__sub_asset_class

    @sub_asset_class.setter
    def sub_asset_class(self, value: dict):
        self._property_changed('sub_asset_class')
        self.__sub_asset_class = value        

    @property
    def provide_mpl_tape_b(self) -> dict:
        return self.__provide_mpl_tape_b

    @provide_mpl_tape_b.setter
    def provide_mpl_tape_b(self, value: dict):
        self._property_changed('provide_mpl_tape_b')
        self.__provide_mpl_tape_b = value        

    @property
    def short_interest(self) -> dict:
        return self.__short_interest

    @short_interest.setter
    def short_interest(self, value: dict):
        self._property_changed('short_interest')
        self.__short_interest = value        

    @property
    def reference_period(self) -> dict:
        return self.__reference_period

    @reference_period.setter
    def reference_period(self, value: dict):
        self._property_changed('reference_period')
        self.__reference_period = value        

    @property
    def provide_mpl_tape_c(self) -> dict:
        return self.__provide_mpl_tape_c

    @provide_mpl_tape_c.setter
    def provide_mpl_tape_c(self, value: dict):
        self._property_changed('provide_mpl_tape_c')
        self.__provide_mpl_tape_c = value        

    @property
    def adjusted_volume(self) -> dict:
        return self.__adjusted_volume

    @adjusted_volume.setter
    def adjusted_volume(self, value: dict):
        self._property_changed('adjusted_volume')
        self.__adjusted_volume = value        

    @property
    def provide_mpl_tape_a(self) -> dict:
        return self.__provide_mpl_tape_a

    @provide_mpl_tape_a.setter
    def provide_mpl_tape_a(self, value: dict):
        self._property_changed('provide_mpl_tape_a')
        self.__provide_mpl_tape_a = value        

    @property
    def pb_client_id(self) -> dict:
        return self.__pb_client_id

    @pb_client_id.setter
    def pb_client_id(self, value: dict):
        self._property_changed('pb_client_id')
        self.__pb_client_id = value        

    @property
    def owner_id(self) -> dict:
        return self.__owner_id

    @owner_id.setter
    def owner_id(self, value: dict):
        self._property_changed('owner_id')
        self.__owner_id = value        

    @property
    def sec_db(self) -> dict:
        return self.__sec_db

    @sec_db.setter
    def sec_db(self, value: dict):
        self._property_changed('sec_db')
        self.__sec_db = value        

    @property
    def composite10_day_adv(self) -> dict:
        return self.__composite10_day_adv

    @composite10_day_adv.setter
    def composite10_day_adv(self, value: dict):
        self._property_changed('composite10_day_adv')
        self.__composite10_day_adv = value        

    @property
    def bpe_quality_stars(self) -> dict:
        return self.__bpe_quality_stars

    @bpe_quality_stars.setter
    def bpe_quality_stars(self, value: dict):
        self._property_changed('bpe_quality_stars')
        self.__bpe_quality_stars = value        

    @property
    def idea_activity_type(self) -> dict:
        return self.__idea_activity_type

    @idea_activity_type.setter
    def idea_activity_type(self, value: dict):
        self._property_changed('idea_activity_type')
        self.__idea_activity_type = value        

    @property
    def idea_source(self) -> dict:
        return self.__idea_source

    @idea_source.setter
    def idea_source(self, value: dict):
        self._property_changed('idea_source')
        self.__idea_source = value        

    @property
    def unadjusted_ask(self) -> dict:
        return self.__unadjusted_ask

    @unadjusted_ask.setter
    def unadjusted_ask(self, value: dict):
        self._property_changed('unadjusted_ask')
        self.__unadjusted_ask = value        

    @property
    def trading_pnl(self) -> dict:
        return self.__trading_pnl

    @trading_pnl.setter
    def trading_pnl(self, value: dict):
        self._property_changed('trading_pnl')
        self.__trading_pnl = value        

    @property
    def collateral_value_required(self) -> dict:
        return self.__collateral_value_required

    @collateral_value_required.setter
    def collateral_value_required(self, value: dict):
        self._property_changed('collateral_value_required')
        self.__collateral_value_required = value        

    @property
    def given_plus_paid(self) -> dict:
        return self.__given_plus_paid

    @given_plus_paid.setter
    def given_plus_paid(self, value: dict):
        self._property_changed('given_plus_paid')
        self.__given_plus_paid = value        

    @property
    def short_conviction_small(self) -> dict:
        return self.__short_conviction_small

    @short_conviction_small.setter
    def short_conviction_small(self, value: dict):
        self._property_changed('short_conviction_small')
        self.__short_conviction_small = value        

    @property
    def price_to_earnings_positive(self) -> dict:
        return self.__price_to_earnings_positive

    @price_to_earnings_positive.setter
    def price_to_earnings_positive(self, value: dict):
        self._property_changed('price_to_earnings_positive')
        self.__price_to_earnings_positive = value        

    @property
    def forecast(self) -> dict:
        return self.__forecast

    @forecast.setter
    def forecast(self, value: dict):
        self._property_changed('forecast')
        self.__forecast = value        

    @property
    def pnl(self) -> dict:
        return self.__pnl

    @pnl.setter
    def pnl(self, value: dict):
        self._property_changed('pnl')
        self.__pnl = value        

    @property
    def upfront_payment_currency(self) -> dict:
        return self.__upfront_payment_currency

    @upfront_payment_currency.setter
    def upfront_payment_currency(self, value: dict):
        self._property_changed('upfront_payment_currency')
        self.__upfront_payment_currency = value        

    @property
    def date_index(self) -> dict:
        return self.__date_index

    @date_index.setter
    def date_index(self, value: dict):
        self._property_changed('date_index')
        self.__date_index = value        

    @property
    def tcm_cost_horizon4_day(self) -> dict:
        return self.__tcm_cost_horizon4_day

    @tcm_cost_horizon4_day.setter
    def tcm_cost_horizon4_day(self, value: dict):
        self._property_changed('tcm_cost_horizon4_day')
        self.__tcm_cost_horizon4_day = value        

    @property
    def asset_classifications_is_primary(self) -> dict:
        return self.__asset_classifications_is_primary

    @asset_classifications_is_primary.setter
    def asset_classifications_is_primary(self, value: dict):
        self._property_changed('asset_classifications_is_primary')
        self.__asset_classifications_is_primary = value        

    @property
    def styles(self) -> dict:
        return self.__styles

    @styles.setter
    def styles(self, value: dict):
        self._property_changed('styles')
        self.__styles = value        

    @property
    def short_name(self) -> dict:
        return self.__short_name

    @short_name.setter
    def short_name(self, value: dict):
        self._property_changed('short_name')
        self.__short_name = value        

    @property
    def dwi_contribution(self) -> dict:
        return self.__dwi_contribution

    @dwi_contribution.setter
    def dwi_contribution(self, value: dict):
        self._property_changed('dwi_contribution')
        self.__dwi_contribution = value        

    @property
    def reset_frequency1(self) -> dict:
        return self.__reset_frequency1

    @reset_frequency1.setter
    def reset_frequency1(self, value: dict):
        self._property_changed('reset_frequency1')
        self.__reset_frequency1 = value        

    @property
    def asset2_id(self) -> dict:
        return self.__asset2_id

    @asset2_id.setter
    def asset2_id(self, value: dict):
        self._property_changed('asset2_id')
        self.__asset2_id = value        

    @property
    def reset_frequency2(self) -> dict:
        return self.__reset_frequency2

    @reset_frequency2.setter
    def reset_frequency2(self, value: dict):
        self._property_changed('reset_frequency2')
        self.__reset_frequency2 = value        

    @property
    def average_fill_price(self) -> dict:
        return self.__average_fill_price

    @average_fill_price.setter
    def average_fill_price(self, value: dict):
        self._property_changed('average_fill_price')
        self.__average_fill_price = value        

    @property
    def price_notation_type2(self) -> dict:
        return self.__price_notation_type2

    @price_notation_type2.setter
    def price_notation_type2(self, value: dict):
        self._property_changed('price_notation_type2')
        self.__price_notation_type2 = value        

    @property
    def price_notation_type3(self) -> dict:
        return self.__price_notation_type3

    @price_notation_type3.setter
    def price_notation_type3(self, value: dict):
        self._property_changed('price_notation_type3')
        self.__price_notation_type3 = value        

    @property
    def bid_gspread(self) -> dict:
        return self.__bid_gspread

    @bid_gspread.setter
    def bid_gspread(self, value: dict):
        self._property_changed('bid_gspread')
        self.__bid_gspread = value        

    @property
    def open_price(self) -> dict:
        return self.__open_price

    @open_price.setter
    def open_price(self, value: dict):
        self._property_changed('open_price')
        self.__open_price = value        

    @property
    def depth_spread_score(self) -> dict:
        return self.__depth_spread_score

    @depth_spread_score.setter
    def depth_spread_score(self, value: dict):
        self._property_changed('depth_spread_score')
        self.__depth_spread_score = value        

    @property
    def sub_account(self) -> dict:
        return self.__sub_account

    @sub_account.setter
    def sub_account(self, value: dict):
        self._property_changed('sub_account')
        self.__sub_account = value        

    @property
    def notional_currency_leg1(self) -> dict:
        return self.__notional_currency_leg1

    @notional_currency_leg1.setter
    def notional_currency_leg1(self, value: dict):
        self._property_changed('notional_currency_leg1')
        self.__notional_currency_leg1 = value        

    @property
    def notional_currency_leg2(self) -> dict:
        return self.__notional_currency_leg2

    @notional_currency_leg2.setter
    def notional_currency_leg2(self, value: dict):
        self._property_changed('notional_currency_leg2')
        self.__notional_currency_leg2 = value        

    @property
    def fair_volatility(self) -> dict:
        return self.__fair_volatility

    @fair_volatility.setter
    def fair_volatility(self, value: dict):
        self._property_changed('fair_volatility')
        self.__fair_volatility = value        

    @property
    def dollar_cross(self) -> dict:
        return self.__dollar_cross

    @dollar_cross.setter
    def dollar_cross(self, value: dict):
        self._property_changed('dollar_cross')
        self.__dollar_cross = value        

    @property
    def portfolio_type(self) -> dict:
        return self.__portfolio_type

    @portfolio_type.setter
    def portfolio_type(self, value: dict):
        self._property_changed('portfolio_type')
        self.__portfolio_type = value        

    @property
    def vendor(self) -> dict:
        return self.__vendor

    @vendor.setter
    def vendor(self, value: dict):
        self._property_changed('vendor')
        self.__vendor = value        

    @property
    def currency(self) -> dict:
        return self.__currency

    @currency.setter
    def currency(self, value: dict):
        self._property_changed('currency')
        self.__currency = value        

    @property
    def cluster_class(self) -> dict:
        return self.__cluster_class

    @cluster_class.setter
    def cluster_class(self, value: dict):
        self._property_changed('cluster_class')
        self.__cluster_class = value        

    @property
    def queueing_time(self) -> dict:
        return self.__queueing_time

    @queueing_time.setter
    def queueing_time(self, value: dict):
        self._property_changed('queueing_time')
        self.__queueing_time = value        

    @property
    def ann_return5_year(self) -> dict:
        return self.__ann_return5_year

    @ann_return5_year.setter
    def ann_return5_year(self, value: dict):
        self._property_changed('ann_return5_year')
        self.__ann_return5_year = value        

    @property
    def bid_size(self) -> dict:
        return self.__bid_size

    @bid_size.setter
    def bid_size(self, value: dict):
        self._property_changed('bid_size')
        self.__bid_size = value        

    @property
    def arrival_mid(self) -> dict:
        return self.__arrival_mid

    @arrival_mid.setter
    def arrival_mid(self, value: dict):
        self._property_changed('arrival_mid')
        self.__arrival_mid = value        

    @property
    def business_sponsor(self) -> dict:
        return self.__business_sponsor

    @business_sponsor.setter
    def business_sponsor(self, value: dict):
        self._property_changed('business_sponsor')
        self.__business_sponsor = value        

    @property
    def asset_parameters_exchange_currency(self) -> dict:
        return self.__asset_parameters_exchange_currency

    @asset_parameters_exchange_currency.setter
    def asset_parameters_exchange_currency(self, value: dict):
        self._property_changed('asset_parameters_exchange_currency')
        self.__asset_parameters_exchange_currency = value        

    @property
    def unexplained(self) -> dict:
        return self.__unexplained

    @unexplained.setter
    def unexplained(self, value: dict):
        self._property_changed('unexplained')
        self.__unexplained = value        

    @property
    def candidate_name(self) -> dict:
        return self.__candidate_name

    @candidate_name.setter
    def candidate_name(self, value: dict):
        self._property_changed('candidate_name')
        self.__candidate_name = value        

    @property
    def metric(self) -> dict:
        return self.__metric

    @metric.setter
    def metric(self, value: dict):
        self._property_changed('metric')
        self.__metric = value        

    @property
    def ask(self) -> dict:
        return self.__ask

    @ask.setter
    def ask(self, value: dict):
        self._property_changed('ask')
        self.__ask = value        

    @property
    def implied_lognormal_volatility(self) -> dict:
        return self.__implied_lognormal_volatility

    @implied_lognormal_volatility.setter
    def implied_lognormal_volatility(self, value: dict):
        self._property_changed('implied_lognormal_volatility')
        self.__implied_lognormal_volatility = value        

    @property
    def close_price(self) -> dict:
        return self.__close_price

    @close_price.setter
    def close_price(self, value: dict):
        self._property_changed('close_price')
        self.__close_price = value        

    @property
    def absolute_strike(self) -> dict:
        return self.__absolute_strike

    @absolute_strike.setter
    def absolute_strike(self, value: dict):
        self._property_changed('absolute_strike')
        self.__absolute_strike = value        

    @property
    def source(self) -> dict:
        return self.__source

    @source.setter
    def source(self, value: dict):
        self._property_changed('source')
        self.__source = value        

    @property
    def asset_classifications_country_code(self) -> dict:
        return self.__asset_classifications_country_code

    @asset_classifications_country_code.setter
    def asset_classifications_country_code(self, value: dict):
        self._property_changed('asset_classifications_country_code')
        self.__asset_classifications_country_code = value        

    @property
    def expense_ratio_net_bps(self) -> dict:
        return self.__expense_ratio_net_bps

    @expense_ratio_net_bps.setter
    def expense_ratio_net_bps(self, value: dict):
        self._property_changed('expense_ratio_net_bps')
        self.__expense_ratio_net_bps = value        

    @property
    def data_set_sub_category(self) -> dict:
        return self.__data_set_sub_category

    @data_set_sub_category.setter
    def data_set_sub_category(self, value: dict):
        self._property_changed('data_set_sub_category')
        self.__data_set_sub_category = value        

    @property
    def day_count_convention2(self) -> dict:
        return self.__day_count_convention2

    @day_count_convention2.setter
    def day_count_convention2(self, value: dict):
        self._property_changed('day_count_convention2')
        self.__day_count_convention2 = value        

    @property
    def quantity_bucket(self) -> dict:
        return self.__quantity_bucket

    @quantity_bucket.setter
    def quantity_bucket(self, value: dict):
        self._property_changed('quantity_bucket')
        self.__quantity_bucket = value        

    @property
    def factor_two(self) -> dict:
        return self.__factor_two

    @factor_two.setter
    def factor_two(self, value: dict):
        self._property_changed('factor_two')
        self.__factor_two = value        

    @property
    def oe_name(self) -> dict:
        return self.__oe_name

    @oe_name.setter
    def oe_name(self, value: dict):
        self._property_changed('oe_name')
        self.__oe_name = value        

    @property
    def given(self) -> dict:
        return self.__given

    @given.setter
    def given(self, value: dict):
        self._property_changed('given')
        self.__given = value        

    @property
    def delisting_date(self) -> dict:
        return self.__delisting_date

    @delisting_date.setter
    def delisting_date(self, value: dict):
        self._property_changed('delisting_date')
        self.__delisting_date = value        

    @property
    def price_spot_target_value(self) -> dict:
        return self.__price_spot_target_value

    @price_spot_target_value.setter
    def price_spot_target_value(self, value: dict):
        self._property_changed('price_spot_target_value')
        self.__price_spot_target_value = value        

    @property
    def weight(self) -> dict:
        return self.__weight

    @weight.setter
    def weight(self, value: dict):
        self._property_changed('weight')
        self.__weight = value        

    @property
    def business_scope(self) -> dict:
        return self.__business_scope

    @business_scope.setter
    def business_scope(self, value: dict):
        self._property_changed('business_scope')
        self.__business_scope = value        

    @property
    def market_data_point(self) -> dict:
        return self.__market_data_point

    @market_data_point.setter
    def market_data_point(self, value: dict):
        self._property_changed('market_data_point')
        self.__market_data_point = value        

    @property
    def absolute_weight(self) -> dict:
        return self.__absolute_weight

    @absolute_weight.setter
    def absolute_weight(self, value: dict):
        self._property_changed('absolute_weight')
        self.__absolute_weight = value        

    @property
    def measure(self) -> dict:
        return self.__measure

    @measure.setter
    def measure(self, value: dict):
        self._property_changed('measure')
        self.__measure = value        

    @property
    def hedge_annualized_volatility(self) -> dict:
        return self.__hedge_annualized_volatility

    @hedge_annualized_volatility.setter
    def hedge_annualized_volatility(self, value: dict):
        self._property_changed('hedge_annualized_volatility')
        self.__hedge_annualized_volatility = value        

    @property
    def benchmark_currency(self) -> dict:
        return self.__benchmark_currency

    @benchmark_currency.setter
    def benchmark_currency(self, value: dict):
        self._property_changed('benchmark_currency')
        self.__benchmark_currency = value        

    @property
    def futures_contract(self) -> dict:
        return self.__futures_contract

    @futures_contract.setter
    def futures_contract(self, value: dict):
        self._property_changed('futures_contract')
        self.__futures_contract = value        

    @property
    def name(self) -> dict:
        return self.__name

    @name.setter
    def name(self, value: dict):
        self._property_changed('name')
        self.__name = value        

    @property
    def aum(self) -> dict:
        return self.__aum

    @aum.setter
    def aum(self, value: dict):
        self._property_changed('aum')
        self.__aum = value        

    @property
    def folder_name(self) -> dict:
        return self.__folder_name

    @folder_name.setter
    def folder_name(self, value: dict):
        self._property_changed('folder_name')
        self.__folder_name = value        

    @property
    def swaption_atm_fwd_rate(self) -> dict:
        return self.__swaption_atm_fwd_rate

    @swaption_atm_fwd_rate.setter
    def swaption_atm_fwd_rate(self, value: dict):
        self._property_changed('swaption_atm_fwd_rate')
        self.__swaption_atm_fwd_rate = value        

    @property
    def live_date(self) -> dict:
        return self.__live_date

    @live_date.setter
    def live_date(self, value: dict):
        self._property_changed('live_date')
        self.__live_date = value        

    @property
    def ask_high(self) -> dict:
        return self.__ask_high

    @ask_high.setter
    def ask_high(self, value: dict):
        self._property_changed('ask_high')
        self.__ask_high = value        

    @property
    def corporate_action_type(self) -> dict:
        return self.__corporate_action_type

    @corporate_action_type.setter
    def corporate_action_type(self, value: dict):
        self._property_changed('corporate_action_type')
        self.__corporate_action_type = value        

    @property
    def prime_id(self) -> dict:
        return self.__prime_id

    @prime_id.setter
    def prime_id(self, value: dict):
        self._property_changed('prime_id')
        self.__prime_id = value        

    @property
    def region_name(self) -> dict:
        return self.__region_name

    @region_name.setter
    def region_name(self, value: dict):
        self._property_changed('region_name')
        self.__region_name = value        

    @property
    def description(self) -> dict:
        return self.__description

    @description.setter
    def description(self, value: dict):
        self._property_changed('description')
        self.__description = value        

    @property
    def asset_classifications_is_country_primary(self) -> dict:
        return self.__asset_classifications_is_country_primary

    @asset_classifications_is_country_primary.setter
    def asset_classifications_is_country_primary(self, value: dict):
        self._property_changed('asset_classifications_is_country_primary')
        self.__asset_classifications_is_country_primary = value        

    @property
    def value_revised(self) -> dict:
        return self.__value_revised

    @value_revised.setter
    def value_revised(self, value: dict):
        self._property_changed('value_revised')
        self.__value_revised = value        

    @property
    def adjusted_trade_price(self) -> dict:
        return self.__adjusted_trade_price

    @adjusted_trade_price.setter
    def adjusted_trade_price(self, value: dict):
        self._property_changed('adjusted_trade_price')
        self.__adjusted_trade_price = value        

    @property
    def is_adr(self) -> dict:
        return self.__is_adr

    @is_adr.setter
    def is_adr(self, value: dict):
        self._property_changed('is_adr')
        self.__is_adr = value        

    @property
    def factor(self) -> dict:
        return self.__factor

    @factor.setter
    def factor(self, value: dict):
        self._property_changed('factor')
        self.__factor = value        

    @property
    def days_on_loan(self) -> dict:
        return self.__days_on_loan

    @days_on_loan.setter
    def days_on_loan(self, value: dict):
        self._property_changed('days_on_loan')
        self.__days_on_loan = value        

    @property
    def long_conviction_small(self) -> dict:
        return self.__long_conviction_small

    @long_conviction_small.setter
    def long_conviction_small(self, value: dict):
        self._property_changed('long_conviction_small')
        self.__long_conviction_small = value        

    @property
    def service_id(self) -> dict:
        return self.__service_id

    @service_id.setter
    def service_id(self, value: dict):
        self._property_changed('service_id')
        self.__service_id = value        

    @property
    def gsfeer(self) -> dict:
        return self.__gsfeer

    @gsfeer.setter
    def gsfeer(self, value: dict):
        self._property_changed('gsfeer')
        self.__gsfeer = value        

    @property
    def wam(self) -> dict:
        return self.__wam

    @wam.setter
    def wam(self, value: dict):
        self._property_changed('wam')
        self.__wam = value        

    @property
    def wal(self) -> dict:
        return self.__wal

    @wal.setter
    def wal(self, value: dict):
        self._property_changed('wal')
        self.__wal = value        

    @property
    def backtest_id(self) -> dict:
        return self.__backtest_id

    @backtest_id.setter
    def backtest_id(self, value: dict):
        self._property_changed('backtest_id')
        self.__backtest_id = value        

    @property
    def leg_two_index_location(self) -> dict:
        return self.__leg_two_index_location

    @leg_two_index_location.setter
    def leg_two_index_location(self, value: dict):
        self._property_changed('leg_two_index_location')
        self.__leg_two_index_location = value        

    @property
    def g_score(self) -> dict:
        return self.__g_score

    @g_score.setter
    def g_score(self, value: dict):
        self._property_changed('g_score')
        self.__g_score = value        

    @property
    def corporate_spread_contribution(self) -> dict:
        return self.__corporate_spread_contribution

    @corporate_spread_contribution.setter
    def corporate_spread_contribution(self, value: dict):
        self._property_changed('corporate_spread_contribution')
        self.__corporate_spread_contribution = value        

    @property
    def market_value(self) -> dict:
        return self.__market_value

    @market_value.setter
    def market_value(self, value: dict):
        self._property_changed('market_value')
        self.__market_value = value        

    @property
    def notional_currency1(self) -> dict:
        return self.__notional_currency1

    @notional_currency1.setter
    def notional_currency1(self, value: dict):
        self._property_changed('notional_currency1')
        self.__notional_currency1 = value        

    @property
    def net_debt_to_ebitda(self) -> dict:
        return self.__net_debt_to_ebitda

    @net_debt_to_ebitda.setter
    def net_debt_to_ebitda(self, value: dict):
        self._property_changed('net_debt_to_ebitda')
        self.__net_debt_to_ebitda = value        

    @property
    def notional_currency2(self) -> dict:
        return self.__notional_currency2

    @notional_currency2.setter
    def notional_currency2(self, value: dict):
        self._property_changed('notional_currency2')
        self.__notional_currency2 = value        

    @property
    def multiple_score(self) -> dict:
        return self.__multiple_score

    @multiple_score.setter
    def multiple_score(self, value: dict):
        self._property_changed('multiple_score')
        self.__multiple_score = value        

    @property
    def beta_adjusted_exposure(self) -> dict:
        return self.__beta_adjusted_exposure

    @beta_adjusted_exposure.setter
    def beta_adjusted_exposure(self, value: dict):
        self._property_changed('beta_adjusted_exposure')
        self.__beta_adjusted_exposure = value        

    @property
    def dividend_points(self) -> dict:
        return self.__dividend_points

    @dividend_points.setter
    def dividend_points(self, value: dict):
        self._property_changed('dividend_points')
        self.__dividend_points = value        

    @property
    def paid(self) -> dict:
        return self.__paid

    @paid.setter
    def paid(self, value: dict):
        self._property_changed('paid')
        self.__paid = value        

    @property
    def short(self) -> dict:
        return self.__short

    @short.setter
    def short(self, value: dict):
        self._property_changed('short')
        self.__short = value        

    @property
    def bos_in_ticks_description(self) -> dict:
        return self.__bos_in_ticks_description

    @bos_in_ticks_description.setter
    def bos_in_ticks_description(self, value: dict):
        self._property_changed('bos_in_ticks_description')
        self.__bos_in_ticks_description = value        

    @property
    def implied_correlation(self) -> dict:
        return self.__implied_correlation

    @implied_correlation.setter
    def implied_correlation(self, value: dict):
        self._property_changed('implied_correlation')
        self.__implied_correlation = value        

    @property
    def normalized_performance(self) -> dict:
        return self.__normalized_performance

    @normalized_performance.setter
    def normalized_performance(self, value: dict):
        self._property_changed('normalized_performance')
        self.__normalized_performance = value        

    @property
    def cm_id(self) -> dict:
        return self.__cm_id

    @cm_id.setter
    def cm_id(self, value: dict):
        self._property_changed('cm_id')
        self.__cm_id = value        

    @property
    def taxonomy(self) -> dict:
        return self.__taxonomy

    @taxonomy.setter
    def taxonomy(self, value: dict):
        self._property_changed('taxonomy')
        self.__taxonomy = value        

    @property
    def swaption_vol(self) -> dict:
        return self.__swaption_vol

    @swaption_vol.setter
    def swaption_vol(self, value: dict):
        self._property_changed('swaption_vol')
        self.__swaption_vol = value        

    @property
    def dividend_yield(self) -> dict:
        return self.__dividend_yield

    @dividend_yield.setter
    def dividend_yield(self, value: dict):
        self._property_changed('dividend_yield')
        self.__dividend_yield = value        

    @property
    def source_origin(self) -> dict:
        return self.__source_origin

    @source_origin.setter
    def source_origin(self, value: dict):
        self._property_changed('source_origin')
        self.__source_origin = value        

    @property
    def measures(self) -> dict:
        return self.__measures

    @measures.setter
    def measures(self, value: dict):
        self._property_changed('measures')
        self.__measures = value        

    @property
    def total_quantity(self) -> dict:
        return self.__total_quantity

    @total_quantity.setter
    def total_quantity(self, value: dict):
        self._property_changed('total_quantity')
        self.__total_quantity = value        

    @property
    def internal_user(self) -> dict:
        return self.__internal_user

    @internal_user.setter
    def internal_user(self, value: dict):
        self._property_changed('internal_user')
        self.__internal_user = value        

    @property
    def underlyer(self) -> dict:
        return self.__underlyer

    @underlyer.setter
    def underlyer(self, value: dict):
        self._property_changed('underlyer')
        self.__underlyer = value        

    @property
    def identifier(self) -> dict:
        return self.__identifier

    @identifier.setter
    def identifier(self, value: dict):
        self._property_changed('identifier')
        self.__identifier = value        

    @property
    def price_unit(self) -> dict:
        return self.__price_unit

    @price_unit.setter
    def price_unit(self, value: dict):
        self._property_changed('price_unit')
        self.__price_unit = value        

    @property
    def redemption_option(self) -> dict:
        return self.__redemption_option

    @redemption_option.setter
    def redemption_option(self, value: dict):
        self._property_changed('redemption_option')
        self.__redemption_option = value        

    @property
    def notional_unit2(self) -> dict:
        return self.__notional_unit2

    @notional_unit2.setter
    def notional_unit2(self, value: dict):
        self._property_changed('notional_unit2')
        self.__notional_unit2 = value        

    @property
    def unadjusted_low(self) -> dict:
        return self.__unadjusted_low

    @unadjusted_low.setter
    def unadjusted_low(self, value: dict):
        self._property_changed('unadjusted_low')
        self.__unadjusted_low = value        

    @property
    def notional_unit1(self) -> dict:
        return self.__notional_unit1

    @notional_unit1.setter
    def notional_unit1(self, value: dict):
        self._property_changed('notional_unit1')
        self.__notional_unit1 = value        

    @property
    def sedol(self) -> dict:
        return self.__sedol

    @sedol.setter
    def sedol(self, value: dict):
        self._property_changed('sedol')
        self.__sedol = value        

    @property
    def rounding_cost_pnl(self) -> dict:
        return self.__rounding_cost_pnl

    @rounding_cost_pnl.setter
    def rounding_cost_pnl(self, value: dict):
        self._property_changed('rounding_cost_pnl')
        self.__rounding_cost_pnl = value        

    @property
    def sustain_global(self) -> dict:
        return self.__sustain_global

    @sustain_global.setter
    def sustain_global(self, value: dict):
        self._property_changed('sustain_global')
        self.__sustain_global = value        

    @property
    def portfolio_id(self) -> dict:
        return self.__portfolio_id

    @portfolio_id.setter
    def portfolio_id(self, value: dict):
        self._property_changed('portfolio_id')
        self.__portfolio_id = value        

    @property
    def ending_date(self) -> dict:
        return self.__ending_date

    @ending_date.setter
    def ending_date(self, value: dict):
        self._property_changed('ending_date')
        self.__ending_date = value        

    @property
    def cap_floor_atm_fwd_rate(self) -> dict:
        return self.__cap_floor_atm_fwd_rate

    @cap_floor_atm_fwd_rate.setter
    def cap_floor_atm_fwd_rate(self, value: dict):
        self._property_changed('cap_floor_atm_fwd_rate')
        self.__cap_floor_atm_fwd_rate = value        

    @property
    def es_percentile(self) -> dict:
        return self.__es_percentile

    @es_percentile.setter
    def es_percentile(self, value: dict):
        self._property_changed('es_percentile')
        self.__es_percentile = value        

    @property
    def ann_return3_year(self) -> dict:
        return self.__ann_return3_year

    @ann_return3_year.setter
    def ann_return3_year(self, value: dict):
        self._property_changed('ann_return3_year')
        self.__ann_return3_year = value        

    @property
    def rcic(self) -> dict:
        return self.__rcic

    @rcic.setter
    def rcic(self, value: dict):
        self._property_changed('rcic')
        self.__rcic = value        

    @property
    def simon_asset_tags(self) -> dict:
        return self.__simon_asset_tags

    @simon_asset_tags.setter
    def simon_asset_tags(self, value: dict):
        self._property_changed('simon_asset_tags')
        self.__simon_asset_tags = value        

    @property
    def forward_point(self) -> dict:
        return self.__forward_point

    @forward_point.setter
    def forward_point(self, value: dict):
        self._property_changed('forward_point')
        self.__forward_point = value        

    @property
    def hit_rate_qtd(self) -> dict:
        return self.__hit_rate_qtd

    @hit_rate_qtd.setter
    def hit_rate_qtd(self, value: dict):
        self._property_changed('hit_rate_qtd')
        self.__hit_rate_qtd = value        

    @property
    def fci(self) -> dict:
        return self.__fci

    @fci.setter
    def fci(self, value: dict):
        self._property_changed('fci')
        self.__fci = value        

    @property
    def recall_quantity(self) -> dict:
        return self.__recall_quantity

    @recall_quantity.setter
    def recall_quantity(self, value: dict):
        self._property_changed('recall_quantity')
        self.__recall_quantity = value        

    @property
    def premium(self) -> dict:
        return self.__premium

    @premium.setter
    def premium(self, value: dict):
        self._property_changed('premium')
        self.__premium = value        

    @property
    def low(self) -> dict:
        return self.__low

    @low.setter
    def low(self, value: dict):
        self._property_changed('low')
        self.__low = value        

    @property
    def cross_group(self) -> dict:
        return self.__cross_group

    @cross_group.setter
    def cross_group(self, value: dict):
        self._property_changed('cross_group')
        self.__cross_group = value        

    @property
    def five_day_price_change_bps(self) -> dict:
        return self.__five_day_price_change_bps

    @five_day_price_change_bps.setter
    def five_day_price_change_bps(self, value: dict):
        self._property_changed('five_day_price_change_bps')
        self.__five_day_price_change_bps = value        

    @property
    def holdings(self) -> dict:
        return self.__holdings

    @holdings.setter
    def holdings(self, value: dict):
        self._property_changed('holdings')
        self.__holdings = value        

    @property
    def price_method(self) -> dict:
        return self.__price_method

    @price_method.setter
    def price_method(self, value: dict):
        self._property_changed('price_method')
        self.__price_method = value        

    @property
    def quoting_style(self) -> dict:
        return self.__quoting_style

    @quoting_style.setter
    def quoting_style(self, value: dict):
        self._property_changed('quoting_style')
        self.__quoting_style = value        

    @property
    def error_message(self) -> dict:
        return self.__error_message

    @error_message.setter
    def error_message(self, value: dict):
        self._property_changed('error_message')
        self.__error_message = value        

    @property
    def mid_price(self) -> dict:
        return self.__mid_price

    @mid_price.setter
    def mid_price(self, value: dict):
        self._property_changed('mid_price')
        self.__mid_price = value        

    @property
    def sts_em_dm(self) -> dict:
        return self.__sts_em_dm

    @sts_em_dm.setter
    def sts_em_dm(self, value: dict):
        self._property_changed('sts_em_dm')
        self.__sts_em_dm = value        

    @property
    def tcm_cost_horizon2_day(self) -> dict:
        return self.__tcm_cost_horizon2_day

    @tcm_cost_horizon2_day.setter
    def tcm_cost_horizon2_day(self, value: dict):
        self._property_changed('tcm_cost_horizon2_day')
        self.__tcm_cost_horizon2_day = value        

    @property
    def pending_loan_count(self) -> dict:
        return self.__pending_loan_count

    @pending_loan_count.setter
    def pending_loan_count(self, value: dict):
        self._property_changed('pending_loan_count')
        self.__pending_loan_count = value        

    @property
    def price_spot_stop_loss_unit(self) -> dict:
        return self.__price_spot_stop_loss_unit

    @price_spot_stop_loss_unit.setter
    def price_spot_stop_loss_unit(self, value: dict):
        self._property_changed('price_spot_stop_loss_unit')
        self.__price_spot_stop_loss_unit = value        

    @property
    def queue_in_lots(self) -> dict:
        return self.__queue_in_lots

    @queue_in_lots.setter
    def queue_in_lots(self, value: dict):
        self._property_changed('queue_in_lots')
        self.__queue_in_lots = value        

    @property
    def price_range_in_ticks_description(self) -> dict:
        return self.__price_range_in_ticks_description

    @price_range_in_ticks_description.setter
    def price_range_in_ticks_description(self, value: dict):
        self._property_changed('price_range_in_ticks_description')
        self.__price_range_in_ticks_description = value        

    @property
    def tender_offer_expiration_date(self) -> dict:
        return self.__tender_offer_expiration_date

    @tender_offer_expiration_date.setter
    def tender_offer_expiration_date(self, value: dict):
        self._property_changed('tender_offer_expiration_date')
        self.__tender_offer_expiration_date = value        

    @property
    def primary_country_ric(self) -> dict:
        return self.__primary_country_ric

    @primary_country_ric.setter
    def primary_country_ric(self, value: dict):
        self._property_changed('primary_country_ric')
        self.__primary_country_ric = value        

    @property
    def leg_one_fixed_payment(self) -> dict:
        return self.__leg_one_fixed_payment

    @leg_one_fixed_payment.setter
    def leg_one_fixed_payment(self, value: dict):
        self._property_changed('leg_one_fixed_payment')
        self.__leg_one_fixed_payment = value        

    @property
    def option_expiration_frequency(self) -> dict:
        return self.__option_expiration_frequency

    @option_expiration_frequency.setter
    def option_expiration_frequency(self, value: dict):
        self._property_changed('option_expiration_frequency')
        self.__option_expiration_frequency = value        

    @property
    def lending_fund_nav_trend(self) -> dict:
        return self.__lending_fund_nav_trend

    @lending_fund_nav_trend.setter
    def lending_fund_nav_trend(self, value: dict):
        self._property_changed('lending_fund_nav_trend')
        self.__lending_fund_nav_trend = value        

    @property
    def tcm_cost_participation_rate5_pct(self) -> dict:
        return self.__tcm_cost_participation_rate5_pct

    @tcm_cost_participation_rate5_pct.setter
    def tcm_cost_participation_rate5_pct(self, value: dict):
        self._property_changed('tcm_cost_participation_rate5_pct')
        self.__tcm_cost_participation_rate5_pct = value        

    @property
    def is_active(self) -> dict:
        return self.__is_active

    @is_active.setter
    def is_active(self, value: dict):
        self._property_changed('is_active')
        self.__is_active = value        

    @property
    def use_machine_learning(self) -> dict:
        return self.__use_machine_learning

    @use_machine_learning.setter
    def use_machine_learning(self, value: dict):
        self._property_changed('use_machine_learning')
        self.__use_machine_learning = value        

    @property
    def growth_score(self) -> dict:
        return self.__growth_score

    @growth_score.setter
    def growth_score(self, value: dict):
        self._property_changed('growth_score')
        self.__growth_score = value        

    @property
    def buffer_threshold(self) -> dict:
        return self.__buffer_threshold

    @buffer_threshold.setter
    def buffer_threshold(self, value: dict):
        self._property_changed('buffer_threshold')
        self.__buffer_threshold = value        

    @property
    def price_forming_continuation_data(self) -> dict:
        return self.__price_forming_continuation_data

    @price_forming_continuation_data.setter
    def price_forming_continuation_data(self, value: dict):
        self._property_changed('price_forming_continuation_data')
        self.__price_forming_continuation_data = value        

    @property
    def adjusted_short_interest(self) -> dict:
        return self.__adjusted_short_interest

    @adjusted_short_interest.setter
    def adjusted_short_interest(self, value: dict):
        self._property_changed('adjusted_short_interest')
        self.__adjusted_short_interest = value        

    @property
    def group(self) -> dict:
        return self.__group

    @group.setter
    def group(self, value: dict):
        self._property_changed('group')
        self.__group = value        

    @property
    def asset_parameters_strike(self) -> dict:
        return self.__asset_parameters_strike

    @asset_parameters_strike.setter
    def asset_parameters_strike(self, value: dict):
        self._property_changed('asset_parameters_strike')
        self.__asset_parameters_strike = value        

    @property
    def asset_parameters_termination_date(self) -> dict:
        return self.__asset_parameters_termination_date

    @asset_parameters_termination_date.setter
    def asset_parameters_termination_date(self, value: dict):
        self._property_changed('asset_parameters_termination_date')
        self.__asset_parameters_termination_date = value        

    @property
    def estimated_spread(self) -> dict:
        return self.__estimated_spread

    @estimated_spread.setter
    def estimated_spread(self, value: dict):
        self._property_changed('estimated_spread')
        self.__estimated_spread = value        

    @property
    def asset_parameters_effective_date(self) -> dict:
        return self.__asset_parameters_effective_date

    @asset_parameters_effective_date.setter
    def asset_parameters_effective_date(self, value: dict):
        self._property_changed('asset_parameters_effective_date')
        self.__asset_parameters_effective_date = value        

    @property
    def ann_return10_year(self) -> dict:
        return self.__ann_return10_year

    @ann_return10_year.setter
    def ann_return10_year(self, value: dict):
        self._property_changed('ann_return10_year')
        self.__ann_return10_year = value        

    @property
    def tcm_cost(self) -> dict:
        return self.__tcm_cost

    @tcm_cost.setter
    def tcm_cost(self, value: dict):
        self._property_changed('tcm_cost')
        self.__tcm_cost = value        

    @property
    def sustain_japan(self) -> dict:
        return self.__sustain_japan

    @sustain_japan.setter
    def sustain_japan(self, value: dict):
        self._property_changed('sustain_japan')
        self.__sustain_japan = value        

    @property
    def fixed_payment_currency_leg1(self) -> dict:
        return self.__fixed_payment_currency_leg1

    @fixed_payment_currency_leg1.setter
    def fixed_payment_currency_leg1(self, value: dict):
        self._property_changed('fixed_payment_currency_leg1')
        self.__fixed_payment_currency_leg1 = value        

    @property
    def hedge_tracking_error(self) -> dict:
        return self.__hedge_tracking_error

    @hedge_tracking_error.setter
    def hedge_tracking_error(self, value: dict):
        self._property_changed('hedge_tracking_error')
        self.__hedge_tracking_error = value        

    @property
    def fixed_payment_currency_leg2(self) -> dict:
        return self.__fixed_payment_currency_leg2

    @fixed_payment_currency_leg2.setter
    def fixed_payment_currency_leg2(self, value: dict):
        self._property_changed('fixed_payment_currency_leg2')
        self.__fixed_payment_currency_leg2 = value        

    @property
    def market_cap_category(self) -> dict:
        return self.__market_cap_category

    @market_cap_category.setter
    def market_cap_category(self, value: dict):
        self._property_changed('market_cap_category')
        self.__market_cap_category = value        

    @property
    def historical_volume(self) -> dict:
        return self.__historical_volume

    @historical_volume.setter
    def historical_volume(self, value: dict):
        self._property_changed('historical_volume')
        self.__historical_volume = value        

    @property
    def strike_price(self) -> dict:
        return self.__strike_price

    @strike_price.setter
    def strike_price(self, value: dict):
        self._property_changed('strike_price')
        self.__strike_price = value        

    @property
    def reset_frequency_leg1(self) -> dict:
        return self.__reset_frequency_leg1

    @reset_frequency_leg1.setter
    def reset_frequency_leg1(self, value: dict):
        self._property_changed('reset_frequency_leg1')
        self.__reset_frequency_leg1 = value        

    @property
    def reset_frequency_leg2(self) -> dict:
        return self.__reset_frequency_leg2

    @reset_frequency_leg2.setter
    def reset_frequency_leg2(self, value: dict):
        self._property_changed('reset_frequency_leg2')
        self.__reset_frequency_leg2 = value        

    @property
    def equity_gamma(self) -> dict:
        return self.__equity_gamma

    @equity_gamma.setter
    def equity_gamma(self, value: dict):
        self._property_changed('equity_gamma')
        self.__equity_gamma = value        

    @property
    def gross_income(self) -> dict:
        return self.__gross_income

    @gross_income.setter
    def gross_income(self, value: dict):
        self._property_changed('gross_income')
        self.__gross_income = value        

    @property
    def em_id(self) -> dict:
        return self.__em_id

    @em_id.setter
    def em_id(self, value: dict):
        self._property_changed('em_id')
        self.__em_id = value        

    @property
    def adjusted_open_price(self) -> dict:
        return self.__adjusted_open_price

    @adjusted_open_price.setter
    def adjusted_open_price(self, value: dict):
        self._property_changed('adjusted_open_price')
        self.__adjusted_open_price = value        

    @property
    def asset_count_in_model(self) -> dict:
        return self.__asset_count_in_model

    @asset_count_in_model.setter
    def asset_count_in_model(self, value: dict):
        self._property_changed('asset_count_in_model')
        self.__asset_count_in_model = value        

    @property
    def sts_credit_region(self) -> dict:
        return self.__sts_credit_region

    @sts_credit_region.setter
    def sts_credit_region(self, value: dict):
        self._property_changed('sts_credit_region')
        self.__sts_credit_region = value        

    @property
    def country_id(self) -> dict:
        return self.__country_id

    @country_id.setter
    def country_id(self, value: dict):
        self._property_changed('country_id')
        self.__country_id = value        

    @property
    def point(self) -> dict:
        return self.__point

    @point.setter
    def point(self, value: dict):
        self._property_changed('point')
        self.__point = value        

    @property
    def total_returns(self) -> dict:
        return self.__total_returns

    @total_returns.setter
    def total_returns(self, value: dict):
        self._property_changed('total_returns')
        self.__total_returns = value        

    @property
    def lender(self) -> dict:
        return self.__lender

    @lender.setter
    def lender(self, value: dict):
        self._property_changed('lender')
        self.__lender = value        

    @property
    def ann_return1_year(self) -> dict:
        return self.__ann_return1_year

    @ann_return1_year.setter
    def ann_return1_year(self, value: dict):
        self._property_changed('ann_return1_year')
        self.__ann_return1_year = value        

    @property
    def min_temperature(self) -> dict:
        return self.__min_temperature

    @min_temperature.setter
    def min_temperature(self, value: dict):
        self._property_changed('min_temperature')
        self.__min_temperature = value        

    @property
    def eff_yield7_day(self) -> dict:
        return self.__eff_yield7_day

    @eff_yield7_day.setter
    def eff_yield7_day(self, value: dict):
        self._property_changed('eff_yield7_day')
        self.__eff_yield7_day = value        

    @property
    def meeting_date(self) -> dict:
        return self.__meeting_date

    @meeting_date.setter
    def meeting_date(self, value: dict):
        self._property_changed('meeting_date')
        self.__meeting_date = value        

    @property
    def relative_strike(self) -> dict:
        return self.__relative_strike

    @relative_strike.setter
    def relative_strike(self, value: dict):
        self._property_changed('relative_strike')
        self.__relative_strike = value        

    @property
    def amount(self) -> dict:
        return self.__amount

    @amount.setter
    def amount(self, value: dict):
        self._property_changed('amount')
        self.__amount = value        

    @property
    def lending_fund_acct(self) -> dict:
        return self.__lending_fund_acct

    @lending_fund_acct.setter
    def lending_fund_acct(self, value: dict):
        self._property_changed('lending_fund_acct')
        self.__lending_fund_acct = value        

    @property
    def rebate(self) -> dict:
        return self.__rebate

    @rebate.setter
    def rebate(self, value: dict):
        self._property_changed('rebate')
        self.__rebate = value        

    @property
    def flagship(self) -> dict:
        return self.__flagship

    @flagship.setter
    def flagship(self, value: dict):
        self._property_changed('flagship')
        self.__flagship = value        

    @property
    def additional_price_notation(self) -> dict:
        return self.__additional_price_notation

    @additional_price_notation.setter
    def additional_price_notation(self, value: dict):
        self._property_changed('additional_price_notation')
        self.__additional_price_notation = value        

    @property
    def factor_category(self) -> dict:
        return self.__factor_category

    @factor_category.setter
    def factor_category(self, value: dict):
        self._property_changed('factor_category')
        self.__factor_category = value        

    @property
    def election_type(self) -> dict:
        return self.__election_type

    @election_type.setter
    def election_type(self, value: dict):
        self._property_changed('election_type')
        self.__election_type = value        

    @property
    def implied_volatility(self) -> dict:
        return self.__implied_volatility

    @implied_volatility.setter
    def implied_volatility(self, value: dict):
        self._property_changed('implied_volatility')
        self.__implied_volatility = value        

    @property
    def spread(self) -> dict:
        return self.__spread

    @spread.setter
    def spread(self, value: dict):
        self._property_changed('spread')
        self.__spread = value        

    @property
    def equity_delta(self) -> dict:
        return self.__equity_delta

    @equity_delta.setter
    def equity_delta(self, value: dict):
        self._property_changed('equity_delta')
        self.__equity_delta = value        

    @property
    def gross_weight(self) -> dict:
        return self.__gross_weight

    @gross_weight.setter
    def gross_weight(self, value: dict):
        self._property_changed('gross_weight')
        self.__gross_weight = value        

    @property
    def listed(self) -> dict:
        return self.__listed

    @listed.setter
    def listed(self, value: dict):
        self._property_changed('listed')
        self.__listed = value        

    @property
    def variance(self) -> dict:
        return self.__variance

    @variance.setter
    def variance(self, value: dict):
        self._property_changed('variance')
        self.__variance = value        

    @property
    def earnings_record_type(self) -> dict:
        return self.__earnings_record_type

    @earnings_record_type.setter
    def earnings_record_type(self, value: dict):
        self._property_changed('earnings_record_type')
        self.__earnings_record_type = value        

    @property
    def g10_currency(self) -> dict:
        return self.__g10_currency

    @g10_currency.setter
    def g10_currency(self, value: dict):
        self._property_changed('g10_currency')
        self.__g10_currency = value        

    @property
    def shock_style(self) -> dict:
        return self.__shock_style

    @shock_style.setter
    def shock_style(self, value: dict):
        self._property_changed('shock_style')
        self.__shock_style = value        

    @property
    def relative_period(self) -> dict:
        return self.__relative_period

    @relative_period.setter
    def relative_period(self, value: dict):
        self._property_changed('relative_period')
        self.__relative_period = value        

    @property
    def methodology(self) -> dict:
        return self.__methodology

    @methodology.setter
    def methodology(self, value: dict):
        self._property_changed('methodology')
        self.__methodology = value        

    @property
    def queue_clock_time_label(self) -> tuple:
        return self.__queue_clock_time_label

    @queue_clock_time_label.setter
    def queue_clock_time_label(self, value: tuple):
        self._property_changed('queue_clock_time_label')
        self.__queue_clock_time_label = value        

    @property
    def market_pnl(self) -> dict:
        return self.__market_pnl

    @market_pnl.setter
    def market_pnl(self, value: dict):
        self._property_changed('market_pnl')
        self.__market_pnl = value        

    @property
    def sustain_asia_ex_japan(self) -> dict:
        return self.__sustain_asia_ex_japan

    @sustain_asia_ex_japan.setter
    def sustain_asia_ex_japan(self, value: dict):
        self._property_changed('sustain_asia_ex_japan')
        self.__sustain_asia_ex_japan = value        

    @property
    def asset_classifications_gics_sub_industry(self) -> dict:
        return self.__asset_classifications_gics_sub_industry

    @asset_classifications_gics_sub_industry.setter
    def asset_classifications_gics_sub_industry(self, value: dict):
        self._property_changed('asset_classifications_gics_sub_industry')
        self.__asset_classifications_gics_sub_industry = value        

    @property
    def index_leg2(self) -> dict:
        return self.__index_leg2

    @index_leg2.setter
    def index_leg2(self, value: dict):
        self._property_changed('index_leg2')
        self.__index_leg2 = value        

    @property
    def neighbour_asset_id(self) -> dict:
        return self.__neighbour_asset_id

    @neighbour_asset_id.setter
    def neighbour_asset_id(self, value: dict):
        self._property_changed('neighbour_asset_id')
        self.__neighbour_asset_id = value        

    @property
    def index_leg1(self) -> dict:
        return self.__index_leg1

    @index_leg1.setter
    def index_leg1(self, value: dict):
        self._property_changed('index_leg1')
        self.__index_leg1 = value        

    @property
    def simon_intl_asset_tags(self) -> dict:
        return self.__simon_intl_asset_tags

    @simon_intl_asset_tags.setter
    def simon_intl_asset_tags(self, value: dict):
        self._property_changed('simon_intl_asset_tags')
        self.__simon_intl_asset_tags = value        

    @property
    def swap_rate(self) -> dict:
        return self.__swap_rate

    @swap_rate.setter
    def swap_rate(self, value: dict):
        self._property_changed('swap_rate')
        self.__swap_rate = value        

    @property
    def path(self) -> dict:
        return self.__path

    @path.setter
    def path(self, value: dict):
        self._property_changed('path')
        self.__path = value        

    @property
    def client_contact(self) -> dict:
        return self.__client_contact

    @client_contact.setter
    def client_contact(self, value: dict):
        self._property_changed('client_contact')
        self.__client_contact = value        

    @property
    def rank(self) -> dict:
        return self.__rank

    @rank.setter
    def rank(self, value: dict):
        self._property_changed('rank')
        self.__rank = value        

    @property
    def mixed_swap_other_reported_sdr(self) -> dict:
        return self.__mixed_swap_other_reported_sdr

    @mixed_swap_other_reported_sdr.setter
    def mixed_swap_other_reported_sdr(self, value: dict):
        self._property_changed('mixed_swap_other_reported_sdr')
        self.__mixed_swap_other_reported_sdr = value        

    @property
    def data_set_category(self) -> dict:
        return self.__data_set_category

    @data_set_category.setter
    def data_set_category(self, value: dict):
        self._property_changed('data_set_category')
        self.__data_set_category = value        

    @property
    def bos_in_bps_label(self) -> tuple:
        return self.__bos_in_bps_label

    @bos_in_bps_label.setter
    def bos_in_bps_label(self, value: tuple):
        self._property_changed('bos_in_bps_label')
        self.__bos_in_bps_label = value        

    @property
    def bos_in_bps(self) -> dict:
        return self.__bos_in_bps

    @bos_in_bps.setter
    def bos_in_bps(self, value: dict):
        self._property_changed('bos_in_bps')
        self.__bos_in_bps = value        

    @property
    def point_class(self) -> dict:
        return self.__point_class

    @point_class.setter
    def point_class(self, value: dict):
        self._property_changed('point_class')
        self.__point_class = value        

    @property
    def fx_spot(self) -> dict:
        return self.__fx_spot

    @fx_spot.setter
    def fx_spot(self, value: dict):
        self._property_changed('fx_spot')
        self.__fx_spot = value        

    @property
    def bid_low(self) -> dict:
        return self.__bid_low

    @bid_low.setter
    def bid_low(self, value: dict):
        self._property_changed('bid_low')
        self.__bid_low = value        

    @property
    def restrict_named_individuals(self) -> dict:
        return self.__restrict_named_individuals

    @restrict_named_individuals.setter
    def restrict_named_individuals(self, value: dict):
        self._property_changed('restrict_named_individuals')
        self.__restrict_named_individuals = value        

    @property
    def fair_variance_volatility(self) -> dict:
        return self.__fair_variance_volatility

    @fair_variance_volatility.setter
    def fair_variance_volatility(self, value: dict):
        self._property_changed('fair_variance_volatility')
        self.__fair_variance_volatility = value        

    @property
    def hedge_volatility(self) -> dict:
        return self.__hedge_volatility

    @hedge_volatility.setter
    def hedge_volatility(self, value: dict):
        self._property_changed('hedge_volatility')
        self.__hedge_volatility = value        

    @property
    def tags(self) -> dict:
        return self.__tags

    @tags.setter
    def tags(self, value: dict):
        self._property_changed('tags')
        self.__tags = value        

    @property
    def underlying_asset_id(self) -> dict:
        return self.__underlying_asset_id

    @underlying_asset_id.setter
    def underlying_asset_id(self, value: dict):
        self._property_changed('underlying_asset_id')
        self.__underlying_asset_id = value        

    @property
    def real_long_rates_contribution(self) -> dict:
        return self.__real_long_rates_contribution

    @real_long_rates_contribution.setter
    def real_long_rates_contribution(self, value: dict):
        self._property_changed('real_long_rates_contribution')
        self.__real_long_rates_contribution = value        

    @property
    def client_exposure(self) -> dict:
        return self.__client_exposure

    @client_exposure.setter
    def client_exposure(self, value: dict):
        self._property_changed('client_exposure')
        self.__client_exposure = value        

    @property
    def gs_sustain_sub_sector(self) -> dict:
        return self.__gs_sustain_sub_sector

    @gs_sustain_sub_sector.setter
    def gs_sustain_sub_sector(self, value: dict):
        self._property_changed('gs_sustain_sub_sector')
        self.__gs_sustain_sub_sector = value        

    @property
    def domain(self) -> dict:
        return self.__domain

    @domain.setter
    def domain(self, value: dict):
        self._property_changed('domain')
        self.__domain = value        

    @property
    def forward_tenor(self) -> dict:
        return self.__forward_tenor

    @forward_tenor.setter
    def forward_tenor(self, value: dict):
        self._property_changed('forward_tenor')
        self.__forward_tenor = value        

    @property
    def jsn(self) -> dict:
        return self.__jsn

    @jsn.setter
    def jsn(self, value: dict):
        self._property_changed('jsn')
        self.__jsn = value        

    @property
    def share_class_assets(self) -> dict:
        return self.__share_class_assets

    @share_class_assets.setter
    def share_class_assets(self, value: dict):
        self._property_changed('share_class_assets')
        self.__share_class_assets = value        

    @property
    def annuity(self) -> dict:
        return self.__annuity

    @annuity.setter
    def annuity(self, value: dict):
        self._property_changed('annuity')
        self.__annuity = value        

    @property
    def quote_type(self) -> dict:
        return self.__quote_type

    @quote_type.setter
    def quote_type(self, value: dict):
        self._property_changed('quote_type')
        self.__quote_type = value        

    @property
    def uid(self) -> dict:
        return self.__uid

    @uid.setter
    def uid(self, value: dict):
        self._property_changed('uid')
        self.__uid = value        

    @property
    def tenor(self) -> dict:
        return self.__tenor

    @tenor.setter
    def tenor(self, value: dict):
        self._property_changed('tenor')
        self.__tenor = value        

    @property
    def es_policy_percentile(self) -> dict:
        return self.__es_policy_percentile

    @es_policy_percentile.setter
    def es_policy_percentile(self, value: dict):
        self._property_changed('es_policy_percentile')
        self.__es_policy_percentile = value        

    @property
    def floating_rate_option(self) -> dict:
        return self.__floating_rate_option

    @floating_rate_option.setter
    def floating_rate_option(self, value: dict):
        self._property_changed('floating_rate_option')
        self.__floating_rate_option = value        

    @property
    def term(self) -> dict:
        return self.__term

    @term.setter
    def term(self, value: dict):
        self._property_changed('term')
        self.__term = value        

    @property
    def restrict_internal_gs_ntk(self) -> dict:
        return self.__restrict_internal_gs_ntk

    @restrict_internal_gs_ntk.setter
    def restrict_internal_gs_ntk(self, value: dict):
        self._property_changed('restrict_internal_gs_ntk')
        self.__restrict_internal_gs_ntk = value        

    @property
    def asset_parameters_clearing_house(self) -> dict:
        return self.__asset_parameters_clearing_house

    @asset_parameters_clearing_house.setter
    def asset_parameters_clearing_house(self, value: dict):
        self._property_changed('asset_parameters_clearing_house')
        self.__asset_parameters_clearing_house = value        

    @property
    def tcm_cost_participation_rate100_pct(self) -> dict:
        return self.__tcm_cost_participation_rate100_pct

    @tcm_cost_participation_rate100_pct.setter
    def tcm_cost_participation_rate100_pct(self, value: dict):
        self._property_changed('tcm_cost_participation_rate100_pct')
        self.__tcm_cost_participation_rate100_pct = value        

    @property
    def disclaimer(self) -> dict:
        return self.__disclaimer

    @disclaimer.setter
    def disclaimer(self, value: dict):
        self._property_changed('disclaimer')
        self.__disclaimer = value        

    @property
    def measure_idx(self) -> dict:
        return self.__measure_idx

    @measure_idx.setter
    def measure_idx(self, value: dict):
        self._property_changed('measure_idx')
        self.__measure_idx = value        

    @property
    def loan_fee(self) -> dict:
        return self.__loan_fee

    @loan_fee.setter
    def loan_fee(self, value: dict):
        self._property_changed('loan_fee')
        self.__loan_fee = value        

    @property
    def deployment_version(self) -> dict:
        return self.__deployment_version

    @deployment_version.setter
    def deployment_version(self, value: dict):
        self._property_changed('deployment_version')
        self.__deployment_version = value        

    @property
    def twi_contribution(self) -> dict:
        return self.__twi_contribution

    @twi_contribution.setter
    def twi_contribution(self, value: dict):
        self._property_changed('twi_contribution')
        self.__twi_contribution = value        

    @property
    def delisted(self) -> dict:
        return self.__delisted

    @delisted.setter
    def delisted(self, value: dict):
        self._property_changed('delisted')
        self.__delisted = value        

    @property
    def regional_focus(self) -> dict:
        return self.__regional_focus

    @regional_focus.setter
    def regional_focus(self, value: dict):
        self._property_changed('regional_focus')
        self.__regional_focus = value        

    @property
    def volume_primary(self) -> dict:
        return self.__volume_primary

    @volume_primary.setter
    def volume_primary(self, value: dict):
        self._property_changed('volume_primary')
        self.__volume_primary = value        

    @property
    def leg_two_delivery_point(self) -> dict:
        return self.__leg_two_delivery_point

    @leg_two_delivery_point.setter
    def leg_two_delivery_point(self, value: dict):
        self._property_changed('leg_two_delivery_point')
        self.__leg_two_delivery_point = value        

    @property
    def funding_bid_price(self) -> dict:
        return self.__funding_bid_price

    @funding_bid_price.setter
    def funding_bid_price(self, value: dict):
        self._property_changed('funding_bid_price')
        self.__funding_bid_price = value        

    @property
    def series(self) -> dict:
        return self.__series

    @series.setter
    def series(self, value: dict):
        self._property_changed('series')
        self.__series = value        

    @property
    def price_to_sales(self) -> dict:
        return self.__price_to_sales

    @price_to_sales.setter
    def price_to_sales(self, value: dict):
        self._property_changed('price_to_sales')
        self.__price_to_sales = value        

    @property
    def closing_auction(self) -> dict:
        return self.__closing_auction

    @closing_auction.setter
    def closing_auction(self, value: dict):
        self._property_changed('closing_auction')
        self.__closing_auction = value        

    @property
    def new_ideas_qtd(self) -> dict:
        return self.__new_ideas_qtd

    @new_ideas_qtd.setter
    def new_ideas_qtd(self, value: dict):
        self._property_changed('new_ideas_qtd')
        self.__new_ideas_qtd = value        

    @property
    def adjusted_ask_price(self) -> dict:
        return self.__adjusted_ask_price

    @adjusted_ask_price.setter
    def adjusted_ask_price(self, value: dict):
        self._property_changed('adjusted_ask_price')
        self.__adjusted_ask_price = value        

    @property
    def quarter(self) -> dict:
        return self.__quarter

    @quarter.setter
    def quarter(self, value: dict):
        self._property_changed('quarter')
        self.__quarter = value        

    @property
    def factor_universe(self) -> dict:
        return self.__factor_universe

    @factor_universe.setter
    def factor_universe(self, value: dict):
        self._property_changed('factor_universe')
        self.__factor_universe = value        

    @property
    def asset_parameters_floating_rate_option(self) -> dict:
        return self.__asset_parameters_floating_rate_option

    @asset_parameters_floating_rate_option.setter
    def asset_parameters_floating_rate_option(self, value: dict):
        self._property_changed('asset_parameters_floating_rate_option')
        self.__asset_parameters_floating_rate_option = value        

    @property
    def arrival_rt(self) -> dict:
        return self.__arrival_rt

    @arrival_rt.setter
    def arrival_rt(self, value: dict):
        self._property_changed('arrival_rt')
        self.__arrival_rt = value        

    @property
    def vote_share(self) -> dict:
        return self.__vote_share

    @vote_share.setter
    def vote_share(self, value: dict):
        self._property_changed('vote_share')
        self.__vote_share = value        

    @property
    def excess_margin_value(self) -> dict:
        return self.__excess_margin_value

    @excess_margin_value.setter
    def excess_margin_value(self, value: dict):
        self._property_changed('excess_margin_value')
        self.__excess_margin_value = value        

    @property
    def transaction_cost(self) -> dict:
        return self.__transaction_cost

    @transaction_cost.setter
    def transaction_cost(self, value: dict):
        self._property_changed('transaction_cost')
        self.__transaction_cost = value        

    @property
    def central_bank_swap_rate(self) -> dict:
        return self.__central_bank_swap_rate

    @central_bank_swap_rate.setter
    def central_bank_swap_rate(self, value: dict):
        self._property_changed('central_bank_swap_rate')
        self.__central_bank_swap_rate = value        

    @property
    def servicing_cost_short_pnl(self) -> dict:
        return self.__servicing_cost_short_pnl

    @servicing_cost_short_pnl.setter
    def servicing_cost_short_pnl(self, value: dict):
        self._property_changed('servicing_cost_short_pnl')
        self.__servicing_cost_short_pnl = value        

    @property
    def notional_unit_leg1(self) -> dict:
        return self.__notional_unit_leg1

    @notional_unit_leg1.setter
    def notional_unit_leg1(self, value: dict):
        self._property_changed('notional_unit_leg1')
        self.__notional_unit_leg1 = value        

    @property
    def cluster_description(self) -> dict:
        return self.__cluster_description

    @cluster_description.setter
    def cluster_description(self, value: dict):
        self._property_changed('cluster_description')
        self.__cluster_description = value        

    @property
    def notional_unit_leg2(self) -> dict:
        return self.__notional_unit_leg2

    @notional_unit_leg2.setter
    def notional_unit_leg2(self, value: dict):
        self._property_changed('notional_unit_leg2')
        self.__notional_unit_leg2 = value        

    @property
    def position_amount(self) -> dict:
        return self.__position_amount

    @position_amount.setter
    def position_amount(self, value: dict):
        self._property_changed('position_amount')
        self.__position_amount = value        

    @property
    def wind_speed(self) -> dict:
        return self.__wind_speed

    @wind_speed.setter
    def wind_speed(self, value: dict):
        self._property_changed('wind_speed')
        self.__wind_speed = value        

    @property
    def ma_rank(self) -> dict:
        return self.__ma_rank

    @ma_rank.setter
    def ma_rank(self, value: dict):
        self._property_changed('ma_rank')
        self.__ma_rank = value        

    @property
    def borrower_id(self) -> dict:
        return self.__borrower_id

    @borrower_id.setter
    def borrower_id(self, value: dict):
        self._property_changed('borrower_id')
        self.__borrower_id = value        

    @property
    def data_product(self) -> dict:
        return self.__data_product

    @data_product.setter
    def data_product(self, value: dict):
        self._property_changed('data_product')
        self.__data_product = value        

    @property
    def implied_volatility_by_delta_strike(self) -> dict:
        return self.__implied_volatility_by_delta_strike

    @implied_volatility_by_delta_strike.setter
    def implied_volatility_by_delta_strike(self, value: dict):
        self._property_changed('implied_volatility_by_delta_strike')
        self.__implied_volatility_by_delta_strike = value        

    @property
    def mq_symbol(self) -> dict:
        return self.__mq_symbol

    @mq_symbol.setter
    def mq_symbol(self, value: dict):
        self._property_changed('mq_symbol')
        self.__mq_symbol = value        

    @property
    def bm_prime_id(self) -> dict:
        return self.__bm_prime_id

    @bm_prime_id.setter
    def bm_prime_id(self, value: dict):
        self._property_changed('bm_prime_id')
        self.__bm_prime_id = value        

    @property
    def corporate_action(self) -> dict:
        return self.__corporate_action

    @corporate_action.setter
    def corporate_action(self, value: dict):
        self._property_changed('corporate_action')
        self.__corporate_action = value        

    @property
    def conviction(self) -> dict:
        return self.__conviction

    @conviction.setter
    def conviction(self, value: dict):
        self._property_changed('conviction')
        self.__conviction = value        

    @property
    def benchmark_maturity(self) -> dict:
        return self.__benchmark_maturity

    @benchmark_maturity.setter
    def benchmark_maturity(self, value: dict):
        self._property_changed('benchmark_maturity')
        self.__benchmark_maturity = value        

    @property
    def gross_flow_normalized(self) -> dict:
        return self.__gross_flow_normalized

    @gross_flow_normalized.setter
    def gross_flow_normalized(self, value: dict):
        self._property_changed('gross_flow_normalized')
        self.__gross_flow_normalized = value        

    @property
    def g_regional_score(self) -> dict:
        return self.__g_regional_score

    @g_regional_score.setter
    def g_regional_score(self, value: dict):
        self._property_changed('g_regional_score')
        self.__g_regional_score = value        

    @property
    def factor_id(self) -> dict:
        return self.__factor_id

    @factor_id.setter
    def factor_id(self, value: dict):
        self._property_changed('factor_id')
        self.__factor_id = value        

    @property
    def hard_to_borrow(self) -> dict:
        return self.__hard_to_borrow

    @hard_to_borrow.setter
    def hard_to_borrow(self, value: dict):
        self._property_changed('hard_to_borrow')
        self.__hard_to_borrow = value        

    @property
    def sts_fx_currency(self) -> dict:
        return self.__sts_fx_currency

    @sts_fx_currency.setter
    def sts_fx_currency(self, value: dict):
        self._property_changed('sts_fx_currency')
        self.__sts_fx_currency = value        

    @property
    def wpk(self) -> dict:
        return self.__wpk

    @wpk.setter
    def wpk(self, value: dict):
        self._property_changed('wpk')
        self.__wpk = value        

    @property
    def bid_change(self) -> dict:
        return self.__bid_change

    @bid_change.setter
    def bid_change(self, value: dict):
        self._property_changed('bid_change')
        self.__bid_change = value        

    @property
    def month(self) -> dict:
        return self.__month

    @month.setter
    def month(self, value: dict):
        self._property_changed('month')
        self.__month = value        

    @property
    def asset_parameters_expiration_date(self) -> dict:
        return self.__asset_parameters_expiration_date

    @asset_parameters_expiration_date.setter
    def asset_parameters_expiration_date(self, value: dict):
        self._property_changed('asset_parameters_expiration_date')
        self.__asset_parameters_expiration_date = value        

    @property
    def expiration(self) -> dict:
        return self.__expiration

    @expiration.setter
    def expiration(self, value: dict):
        self._property_changed('expiration')
        self.__expiration = value        

    @property
    def country_name(self) -> dict:
        return self.__country_name

    @country_name.setter
    def country_name(self, value: dict):
        self._property_changed('country_name')
        self.__country_name = value        

    @property
    def starting_date(self) -> dict:
        return self.__starting_date

    @starting_date.setter
    def starting_date(self, value: dict):
        self._property_changed('starting_date')
        self.__starting_date = value        

    @property
    def loan_id(self) -> dict:
        return self.__loan_id

    @loan_id.setter
    def loan_id(self, value: dict):
        self._property_changed('loan_id')
        self.__loan_id = value        

    @property
    def onboarded(self) -> dict:
        return self.__onboarded

    @onboarded.setter
    def onboarded(self, value: dict):
        self._property_changed('onboarded')
        self.__onboarded = value        

    @property
    def liquidity_score(self) -> dict:
        return self.__liquidity_score

    @liquidity_score.setter
    def liquidity_score(self, value: dict):
        self._property_changed('liquidity_score')
        self.__liquidity_score = value        

    @property
    def spread_leg2(self) -> dict:
        return self.__spread_leg2

    @spread_leg2.setter
    def spread_leg2(self, value: dict):
        self._property_changed('spread_leg2')
        self.__spread_leg2 = value        

    @property
    def spread_leg1(self) -> dict:
        return self.__spread_leg1

    @spread_leg1.setter
    def spread_leg1(self, value: dict):
        self._property_changed('spread_leg1')
        self.__spread_leg1 = value        

    @property
    def long_rates_contribution(self) -> dict:
        return self.__long_rates_contribution

    @long_rates_contribution.setter
    def long_rates_contribution(self, value: dict):
        self._property_changed('long_rates_contribution')
        self.__long_rates_contribution = value        

    @property
    def importance(self) -> dict:
        return self.__importance

    @importance.setter
    def importance(self, value: dict):
        self._property_changed('importance')
        self.__importance = value        

    @property
    def source_date_span(self) -> dict:
        return self.__source_date_span

    @source_date_span.setter
    def source_date_span(self, value: dict):
        self._property_changed('source_date_span')
        self.__source_date_span = value        

    @property
    def asset_classifications_gics_sector(self) -> dict:
        return self.__asset_classifications_gics_sector

    @asset_classifications_gics_sector.setter
    def asset_classifications_gics_sector(self, value: dict):
        self._property_changed('asset_classifications_gics_sector')
        self.__asset_classifications_gics_sector = value        

    @property
    def ann_yield6_month(self) -> dict:
        return self.__ann_yield6_month

    @ann_yield6_month.setter
    def ann_yield6_month(self, value: dict):
        self._property_changed('ann_yield6_month')
        self.__ann_yield6_month = value        

    @property
    def underlying_data_set_id(self) -> dict:
        return self.__underlying_data_set_id

    @underlying_data_set_id.setter
    def underlying_data_set_id(self, value: dict):
        self._property_changed('underlying_data_set_id')
        self.__underlying_data_set_id = value        

    @property
    def sts_asset_name(self) -> dict:
        return self.__sts_asset_name

    @sts_asset_name.setter
    def sts_asset_name(self, value: dict):
        self._property_changed('sts_asset_name')
        self.__sts_asset_name = value        

    @property
    def close_unadjusted(self) -> dict:
        return self.__close_unadjusted

    @close_unadjusted.setter
    def close_unadjusted(self, value: dict):
        self._property_changed('close_unadjusted')
        self.__close_unadjusted = value        

    @property
    def value_unit(self) -> dict:
        return self.__value_unit

    @value_unit.setter
    def value_unit(self, value: dict):
        self._property_changed('value_unit')
        self.__value_unit = value        

    @property
    def quantity_unit(self) -> dict:
        return self.__quantity_unit

    @quantity_unit.setter
    def quantity_unit(self, value: dict):
        self._property_changed('quantity_unit')
        self.__quantity_unit = value        

    @property
    def adjusted_low_price(self) -> dict:
        return self.__adjusted_low_price

    @adjusted_low_price.setter
    def adjusted_low_price(self, value: dict):
        self._property_changed('adjusted_low_price')
        self.__adjusted_low_price = value        

    @property
    def net_exposure_classification(self) -> dict:
        return self.__net_exposure_classification

    @net_exposure_classification.setter
    def net_exposure_classification(self, value: dict):
        self._property_changed('net_exposure_classification')
        self.__net_exposure_classification = value        

    @property
    def settlement_method(self) -> dict:
        return self.__settlement_method

    @settlement_method.setter
    def settlement_method(self, value: dict):
        self._property_changed('settlement_method')
        self.__settlement_method = value        

    @property
    def long_conviction_large(self) -> dict:
        return self.__long_conviction_large

    @long_conviction_large.setter
    def long_conviction_large(self, value: dict):
        self._property_changed('long_conviction_large')
        self.__long_conviction_large = value        

    @property
    def oad(self) -> dict:
        return self.__oad

    @oad.setter
    def oad(self, value: dict):
        self._property_changed('oad')
        self.__oad = value        

    @property
    def load(self) -> dict:
        return self.__load

    @load.setter
    def load(self, value: dict):
        self._property_changed('load')
        self.__load = value        

    @property
    def rate(self) -> dict:
        return self.__rate

    @rate.setter
    def rate(self, value: dict):
        self._property_changed('rate')
        self.__rate = value        

    @property
    def alpha(self) -> dict:
        return self.__alpha

    @alpha.setter
    def alpha(self, value: dict):
        self._property_changed('alpha')
        self.__alpha = value        

    @property
    def client(self) -> dict:
        return self.__client

    @client.setter
    def client(self, value: dict):
        self._property_changed('client')
        self.__client = value        

    @property
    def company(self) -> dict:
        return self.__company

    @company.setter
    def company(self, value: dict):
        self._property_changed('company')
        self.__company = value        

    @property
    def conviction_list(self) -> dict:
        return self.__conviction_list

    @conviction_list.setter
    def conviction_list(self, value: dict):
        self._property_changed('conviction_list')
        self.__conviction_list = value        

    @property
    def settlement_frequency(self) -> dict:
        return self.__settlement_frequency

    @settlement_frequency.setter
    def settlement_frequency(self, value: dict):
        self._property_changed('settlement_frequency')
        self.__settlement_frequency = value        

    @property
    def dist_avg7_day(self) -> dict:
        return self.__dist_avg7_day

    @dist_avg7_day.setter
    def dist_avg7_day(self, value: dict):
        self._property_changed('dist_avg7_day')
        self.__dist_avg7_day = value        

    @property
    def remove_tape_c(self) -> dict:
        return self.__remove_tape_c

    @remove_tape_c.setter
    def remove_tape_c(self, value: dict):
        self._property_changed('remove_tape_c')
        self.__remove_tape_c = value        

    @property
    def remove_tape_b(self) -> dict:
        return self.__remove_tape_b

    @remove_tape_b.setter
    def remove_tape_b(self, value: dict):
        self._property_changed('remove_tape_b')
        self.__remove_tape_b = value        

    @property
    def in_risk_model(self) -> dict:
        return self.__in_risk_model

    @in_risk_model.setter
    def in_risk_model(self, value: dict):
        self._property_changed('in_risk_model')
        self.__in_risk_model = value        

    @property
    def daily_net_shareholder_flows_percent(self) -> dict:
        return self.__daily_net_shareholder_flows_percent

    @daily_net_shareholder_flows_percent.setter
    def daily_net_shareholder_flows_percent(self, value: dict):
        self._property_changed('daily_net_shareholder_flows_percent')
        self.__daily_net_shareholder_flows_percent = value        

    @property
    def type_of_return(self) -> dict:
        return self.__type_of_return

    @type_of_return.setter
    def type_of_return(self, value: dict):
        self._property_changed('type_of_return')
        self.__type_of_return = value        

    @property
    def servicing_cost_long_pnl(self) -> dict:
        return self.__servicing_cost_long_pnl

    @servicing_cost_long_pnl.setter
    def servicing_cost_long_pnl(self, value: dict):
        self._property_changed('servicing_cost_long_pnl')
        self.__servicing_cost_long_pnl = value        

    @property
    def excess_margin_percentage(self) -> dict:
        return self.__excess_margin_percentage

    @excess_margin_percentage.setter
    def excess_margin_percentage(self, value: dict):
        self._property_changed('excess_margin_percentage')
        self.__excess_margin_percentage = value        

    @property
    def remove_tape_a(self) -> dict:
        return self.__remove_tape_a

    @remove_tape_a.setter
    def remove_tape_a(self, value: dict):
        self._property_changed('remove_tape_a')
        self.__remove_tape_a = value        

    @property
    def meeting_number(self) -> dict:
        return self.__meeting_number

    @meeting_number.setter
    def meeting_number(self, value: dict):
        self._property_changed('meeting_number')
        self.__meeting_number = value        

    @property
    def exchange_id(self) -> dict:
        return self.__exchange_id

    @exchange_id.setter
    def exchange_id(self, value: dict):
        self._property_changed('exchange_id')
        self.__exchange_id = value        

    @property
    def mid_gspread(self) -> dict:
        return self.__mid_gspread

    @mid_gspread.setter
    def mid_gspread(self, value: dict):
        self._property_changed('mid_gspread')
        self.__mid_gspread = value        

    @property
    def tcm_cost_horizon20_day(self) -> dict:
        return self.__tcm_cost_horizon20_day

    @tcm_cost_horizon20_day.setter
    def tcm_cost_horizon20_day(self, value: dict):
        self._property_changed('tcm_cost_horizon20_day')
        self.__tcm_cost_horizon20_day = value        

    @property
    def long_level(self) -> dict:
        return self.__long_level

    @long_level.setter
    def long_level(self, value: dict):
        self._property_changed('long_level')
        self.__long_level = value        

    @property
    def realm(self) -> dict:
        return self.__realm

    @realm.setter
    def realm(self, value: dict):
        self._property_changed('realm')
        self.__realm = value        

    @property
    def bid(self) -> dict:
        return self.__bid

    @bid.setter
    def bid(self, value: dict):
        self._property_changed('bid')
        self.__bid = value        

    @property
    def data_description(self) -> dict:
        return self.__data_description

    @data_description.setter
    def data_description(self, value: dict):
        self._property_changed('data_description')
        self.__data_description = value        

    @property
    def is_aggressive(self) -> dict:
        return self.__is_aggressive

    @is_aggressive.setter
    def is_aggressive(self, value: dict):
        self._property_changed('is_aggressive')
        self.__is_aggressive = value        

    @property
    def order_id(self) -> dict:
        return self.__order_id

    @order_id.setter
    def order_id(self, value: dict):
        self._property_changed('order_id')
        self.__order_id = value        

    @property
    def gsideid(self) -> dict:
        return self.__gsideid

    @gsideid.setter
    def gsideid(self, value: dict):
        self._property_changed('gsideid')
        self.__gsideid = value        

    @property
    def repo_rate(self) -> dict:
        return self.__repo_rate

    @repo_rate.setter
    def repo_rate(self, value: dict):
        self._property_changed('repo_rate')
        self.__repo_rate = value        

    @property
    def division(self) -> dict:
        return self.__division

    @division.setter
    def division(self, value: dict):
        self._property_changed('division')
        self.__division = value        

    @property
    def market_cap_usd(self) -> dict:
        return self.__market_cap_usd

    @market_cap_usd.setter
    def market_cap_usd(self, value: dict):
        self._property_changed('market_cap_usd')
        self.__market_cap_usd = value        

    @property
    def high_price(self) -> dict:
        return self.__high_price

    @high_price.setter
    def high_price(self, value: dict):
        self._property_changed('high_price')
        self.__high_price = value        

    @property
    def absolute_shares(self) -> dict:
        return self.__absolute_shares

    @absolute_shares.setter
    def absolute_shares(self, value: dict):
        self._property_changed('absolute_shares')
        self.__absolute_shares = value        

    @property
    def action(self) -> dict:
        return self.__action

    @action.setter
    def action(self, value: dict):
        self._property_changed('action')
        self.__action = value        

    @property
    def model(self) -> dict:
        return self.__model

    @model.setter
    def model(self, value: dict):
        self._property_changed('model')
        self.__model = value        

    @property
    def id(self) -> dict:
        return self.__id

    @id.setter
    def id(self, value: dict):
        self._property_changed('id')
        self.__id = value        

    @property
    def arrival_haircut_vwap_normalized(self) -> dict:
        return self.__arrival_haircut_vwap_normalized

    @arrival_haircut_vwap_normalized.setter
    def arrival_haircut_vwap_normalized(self, value: dict):
        self._property_changed('arrival_haircut_vwap_normalized')
        self.__arrival_haircut_vwap_normalized = value        

    @property
    def price_component(self) -> dict:
        return self.__price_component

    @price_component.setter
    def price_component(self, value: dict):
        self._property_changed('price_component')
        self.__price_component = value        

    @property
    def queue_clock_time_description(self) -> dict:
        return self.__queue_clock_time_description

    @queue_clock_time_description.setter
    def queue_clock_time_description(self, value: dict):
        self._property_changed('queue_clock_time_description')
        self.__queue_clock_time_description = value        

    @property
    def delta_strike(self) -> dict:
        return self.__delta_strike

    @delta_strike.setter
    def delta_strike(self, value: dict):
        self._property_changed('delta_strike')
        self.__delta_strike = value        

    @property
    def asset_parameters_notional_currency(self) -> dict:
        return self.__asset_parameters_notional_currency

    @asset_parameters_notional_currency.setter
    def asset_parameters_notional_currency(self, value: dict):
        self._property_changed('asset_parameters_notional_currency')
        self.__asset_parameters_notional_currency = value        

    @property
    def value_actual(self) -> dict:
        return self.__value_actual

    @value_actual.setter
    def value_actual(self, value: dict):
        self._property_changed('value_actual')
        self.__value_actual = value        

    @property
    def upi(self) -> dict:
        return self.__upi

    @upi.setter
    def upi(self, value: dict):
        self._property_changed('upi')
        self.__upi = value        

    @property
    def asset_types(self) -> dict:
        return self.__asset_types

    @asset_types.setter
    def asset_types(self, value: dict):
        self._property_changed('asset_types')
        self.__asset_types = value        

    @property
    def bcid(self) -> dict:
        return self.__bcid

    @bcid.setter
    def bcid(self, value: dict):
        self._property_changed('bcid')
        self.__bcid = value        

    @property
    def mkt_point(self) -> dict:
        return self.__mkt_point

    @mkt_point.setter
    def mkt_point(self, value: dict):
        self._property_changed('mkt_point')
        self.__mkt_point = value        

    @property
    def collateral_currency(self) -> dict:
        return self.__collateral_currency

    @collateral_currency.setter
    def collateral_currency(self, value: dict):
        self._property_changed('collateral_currency')
        self.__collateral_currency = value        

    @property
    def original_country(self) -> dict:
        return self.__original_country

    @original_country.setter
    def original_country(self, value: dict):
        self._property_changed('original_country')
        self.__original_country = value        

    @property
    def touch_liquidity_score(self) -> dict:
        return self.__touch_liquidity_score

    @touch_liquidity_score.setter
    def touch_liquidity_score(self, value: dict):
        self._property_changed('touch_liquidity_score')
        self.__touch_liquidity_score = value        

    @property
    def field(self) -> dict:
        return self.__field

    @field.setter
    def field(self, value: dict):
        self._property_changed('field')
        self.__field = value        

    @property
    def factor_category_id(self) -> dict:
        return self.__factor_category_id

    @factor_category_id.setter
    def factor_category_id(self, value: dict):
        self._property_changed('factor_category_id')
        self.__factor_category_id = value        

    @property
    def expected_completion_date(self) -> dict:
        return self.__expected_completion_date

    @expected_completion_date.setter
    def expected_completion_date(self, value: dict):
        self._property_changed('expected_completion_date')
        self.__expected_completion_date = value        

    @property
    def spread_option_vol(self) -> dict:
        return self.__spread_option_vol

    @spread_option_vol.setter
    def spread_option_vol(self, value: dict):
        self._property_changed('spread_option_vol')
        self.__spread_option_vol = value        

    @property
    def inflation_swap_rate(self) -> dict:
        return self.__inflation_swap_rate

    @inflation_swap_rate.setter
    def inflation_swap_rate(self, value: dict):
        self._property_changed('inflation_swap_rate')
        self.__inflation_swap_rate = value        

    @property
    def fx_risk_premium_index(self) -> dict:
        return self.__fx_risk_premium_index

    @fx_risk_premium_index.setter
    def fx_risk_premium_index(self, value: dict):
        self._property_changed('fx_risk_premium_index')
        self.__fx_risk_premium_index = value        

    @property
    def skew(self) -> dict:
        return self.__skew

    @skew.setter
    def skew(self, value: dict):
        self._property_changed('skew')
        self.__skew = value        

    @property
    def status(self) -> dict:
        return self.__status

    @status.setter
    def status(self, value: dict):
        self._property_changed('status')
        self.__status = value        

    @property
    def sustain_emerging_markets(self) -> dict:
        return self.__sustain_emerging_markets

    @sustain_emerging_markets.setter
    def sustain_emerging_markets(self, value: dict):
        self._property_changed('sustain_emerging_markets')
        self.__sustain_emerging_markets = value        

    @property
    def total_price(self) -> dict:
        return self.__total_price

    @total_price.setter
    def total_price(self, value: dict):
        self._property_changed('total_price')
        self.__total_price = value        

    @property
    def embeded_option(self) -> dict:
        return self.__embeded_option

    @embeded_option.setter
    def embeded_option(self, value: dict):
        self._property_changed('embeded_option')
        self.__embeded_option = value        

    @property
    def event_source(self) -> dict:
        return self.__event_source

    @event_source.setter
    def event_source(self, value: dict):
        self._property_changed('event_source')
        self.__event_source = value        

    @property
    def on_behalf_of(self) -> dict:
        return self.__on_behalf_of

    @on_behalf_of.setter
    def on_behalf_of(self, value: dict):
        self._property_changed('on_behalf_of')
        self.__on_behalf_of = value        

    @property
    def qis_perm_no(self) -> dict:
        return self.__qis_perm_no

    @qis_perm_no.setter
    def qis_perm_no(self, value: dict):
        self._property_changed('qis_perm_no')
        self.__qis_perm_no = value        

    @property
    def shareclass_id(self) -> dict:
        return self.__shareclass_id

    @shareclass_id.setter
    def shareclass_id(self, value: dict):
        self._property_changed('shareclass_id')
        self.__shareclass_id = value        

    @property
    def sts_commodity_sector(self) -> dict:
        return self.__sts_commodity_sector

    @sts_commodity_sector.setter
    def sts_commodity_sector(self, value: dict):
        self._property_changed('sts_commodity_sector')
        self.__sts_commodity_sector = value        

    @property
    def exception_status(self) -> dict:
        return self.__exception_status

    @exception_status.setter
    def exception_status(self, value: dict):
        self._property_changed('exception_status')
        self.__exception_status = value        

    @property
    def sales_coverage(self) -> dict:
        return self.__sales_coverage

    @sales_coverage.setter
    def sales_coverage(self, value: dict):
        self._property_changed('sales_coverage')
        self.__sales_coverage = value        

    @property
    def short_exposure(self) -> dict:
        return self.__short_exposure

    @short_exposure.setter
    def short_exposure(self, value: dict):
        self._property_changed('short_exposure')
        self.__short_exposure = value        

    @property
    def tcm_cost_participation_rate10_pct(self) -> dict:
        return self.__tcm_cost_participation_rate10_pct

    @tcm_cost_participation_rate10_pct.setter
    def tcm_cost_participation_rate10_pct(self, value: dict):
        self._property_changed('tcm_cost_participation_rate10_pct')
        self.__tcm_cost_participation_rate10_pct = value        

    @property
    def event_time(self) -> dict:
        return self.__event_time

    @event_time.setter
    def event_time(self, value: dict):
        self._property_changed('event_time')
        self.__event_time = value        

    @property
    def position_source_name(self) -> dict:
        return self.__position_source_name

    @position_source_name.setter
    def position_source_name(self, value: dict):
        self._property_changed('position_source_name')
        self.__position_source_name = value        

    @property
    def arrival_haircut_vwap(self) -> dict:
        return self.__arrival_haircut_vwap

    @arrival_haircut_vwap.setter
    def arrival_haircut_vwap(self, value: dict):
        self._property_changed('arrival_haircut_vwap')
        self.__arrival_haircut_vwap = value        

    @property
    def interest_rate(self) -> dict:
        return self.__interest_rate

    @interest_rate.setter
    def interest_rate(self, value: dict):
        self._property_changed('interest_rate')
        self.__interest_rate = value        

    @property
    def execution_days(self) -> dict:
        return self.__execution_days

    @execution_days.setter
    def execution_days(self, value: dict):
        self._property_changed('execution_days')
        self.__execution_days = value        

    @property
    def side(self) -> dict:
        return self.__side

    @side.setter
    def side(self, value: dict):
        self._property_changed('side')
        self.__side = value        

    @property
    def compliance_restricted_status(self) -> dict:
        return self.__compliance_restricted_status

    @compliance_restricted_status.setter
    def compliance_restricted_status(self, value: dict):
        self._property_changed('compliance_restricted_status')
        self.__compliance_restricted_status = value        

    @property
    def forward(self) -> dict:
        return self.__forward

    @forward.setter
    def forward(self, value: dict):
        self._property_changed('forward')
        self.__forward = value        

    @property
    def borrow_fee(self) -> dict:
        return self.__borrow_fee

    @borrow_fee.setter
    def borrow_fee(self, value: dict):
        self._property_changed('borrow_fee')
        self.__borrow_fee = value        

    @property
    def strike(self) -> dict:
        return self.__strike

    @strike.setter
    def strike(self, value: dict):
        self._property_changed('strike')
        self.__strike = value        

    @property
    def loan_spread(self) -> dict:
        return self.__loan_spread

    @loan_spread.setter
    def loan_spread(self, value: dict):
        self._property_changed('loan_spread')
        self.__loan_spread = value        

    @property
    def tcm_cost_horizon12_hour(self) -> dict:
        return self.__tcm_cost_horizon12_hour

    @tcm_cost_horizon12_hour.setter
    def tcm_cost_horizon12_hour(self, value: dict):
        self._property_changed('tcm_cost_horizon12_hour')
        self.__tcm_cost_horizon12_hour = value        

    @property
    def dew_point(self) -> dict:
        return self.__dew_point

    @dew_point.setter
    def dew_point(self, value: dict):
        self._property_changed('dew_point')
        self.__dew_point = value        

    @property
    def research_commission(self) -> dict:
        return self.__research_commission

    @research_commission.setter
    def research_commission(self, value: dict):
        self._property_changed('research_commission')
        self.__research_commission = value        

    @property
    def leg_one_delivery_point(self) -> dict:
        return self.__leg_one_delivery_point

    @leg_one_delivery_point.setter
    def leg_one_delivery_point(self, value: dict):
        self._property_changed('leg_one_delivery_point')
        self.__leg_one_delivery_point = value        

    @property
    def asset_classifications_risk_country_code(self) -> dict:
        return self.__asset_classifications_risk_country_code

    @asset_classifications_risk_country_code.setter
    def asset_classifications_risk_country_code(self, value: dict):
        self._property_changed('asset_classifications_risk_country_code')
        self.__asset_classifications_risk_country_code = value        

    @property
    def event_status(self) -> dict:
        return self.__event_status

    @event_status.setter
    def event_status(self, value: dict):
        self._property_changed('event_status')
        self.__event_status = value        

    @property
    def asset_parameters_settlement(self) -> dict:
        return self.__asset_parameters_settlement

    @asset_parameters_settlement.setter
    def asset_parameters_settlement(self, value: dict):
        self._property_changed('asset_parameters_settlement')
        self.__asset_parameters_settlement = value        

    @property
    def return_(self) -> dict:
        return self.__return

    @return_.setter
    def return_(self, value: dict):
        self._property_changed('return_')
        self.__return = value        

    @property
    def max_temperature(self) -> dict:
        return self.__max_temperature

    @max_temperature.setter
    def max_temperature(self, value: dict):
        self._property_changed('max_temperature')
        self.__max_temperature = value        

    @property
    def acquirer_shareholder_meeting_date(self) -> dict:
        return self.__acquirer_shareholder_meeting_date

    @acquirer_shareholder_meeting_date.setter
    def acquirer_shareholder_meeting_date(self, value: dict):
        self._property_changed('acquirer_shareholder_meeting_date')
        self.__acquirer_shareholder_meeting_date = value        

    @property
    def notional_amount(self) -> dict:
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: dict):
        self._property_changed('notional_amount')
        self.__notional_amount = value        

    @property
    def pay_or_receive(self) -> dict:
        return self.__pay_or_receive

    @pay_or_receive.setter
    def pay_or_receive(self, value: dict):
        self._property_changed('pay_or_receive')
        self.__pay_or_receive = value        

    @property
    def arrival_rt_normalized(self) -> dict:
        return self.__arrival_rt_normalized

    @arrival_rt_normalized.setter
    def arrival_rt_normalized(self, value: dict):
        self._property_changed('arrival_rt_normalized')
        self.__arrival_rt_normalized = value        

    @property
    def report_type(self) -> dict:
        return self.__report_type

    @report_type.setter
    def report_type(self, value: dict):
        self._property_changed('report_type')
        self.__report_type = value        

    @property
    def source_url(self) -> dict:
        return self.__source_url

    @source_url.setter
    def source_url(self, value: dict):
        self._property_changed('source_url')
        self.__source_url = value        

    @property
    def estimated_return(self) -> dict:
        return self.__estimated_return

    @estimated_return.setter
    def estimated_return(self, value: dict):
        self._property_changed('estimated_return')
        self.__estimated_return = value        

    @property
    def high(self) -> dict:
        return self.__high

    @high.setter
    def high(self, value: dict):
        self._property_changed('high')
        self.__high = value        

    @property
    def source_last_update(self) -> dict:
        return self.__source_last_update

    @source_last_update.setter
    def source_last_update(self, value: dict):
        self._property_changed('source_last_update')
        self.__source_last_update = value        

    @property
    def quantity_mw(self) -> dict:
        return self.__quantity_mw

    @quantity_mw.setter
    def quantity_mw(self, value: dict):
        self._property_changed('quantity_mw')
        self.__quantity_mw = value        

    @property
    def pnode_id(self) -> dict:
        return self.__pnode_id

    @pnode_id.setter
    def pnode_id(self, value: dict):
        self._property_changed('pnode_id')
        self.__pnode_id = value        

    @property
    def event_name(self) -> dict:
        return self.__event_name

    @event_name.setter
    def event_name(self, value: dict):
        self._property_changed('event_name')
        self.__event_name = value        

    @property
    def indication_of_other_price_affecting_term(self) -> dict:
        return self.__indication_of_other_price_affecting_term

    @indication_of_other_price_affecting_term.setter
    def indication_of_other_price_affecting_term(self, value: dict):
        self._property_changed('indication_of_other_price_affecting_term')
        self.__indication_of_other_price_affecting_term = value        

    @property
    def unadjusted_bid(self) -> dict:
        return self.__unadjusted_bid

    @unadjusted_bid.setter
    def unadjusted_bid(self, value: dict):
        self._property_changed('unadjusted_bid')
        self.__unadjusted_bid = value        

    @property
    def backtest_type(self) -> dict:
        return self.__backtest_type

    @backtest_type.setter
    def backtest_type(self, value: dict):
        self._property_changed('backtest_type')
        self.__backtest_type = value        

    @property
    def gsdeer(self) -> dict:
        return self.__gsdeer

    @gsdeer.setter
    def gsdeer(self, value: dict):
        self._property_changed('gsdeer')
        self.__gsdeer = value        

    @property
    def g_regional_percentile(self) -> dict:
        return self.__g_regional_percentile

    @g_regional_percentile.setter
    def g_regional_percentile(self, value: dict):
        self._property_changed('g_regional_percentile')
        self.__g_regional_percentile = value        

    @property
    def prev_close_ask(self) -> dict:
        return self.__prev_close_ask

    @prev_close_ask.setter
    def prev_close_ask(self, value: dict):
        self._property_changed('prev_close_ask')
        self.__prev_close_ask = value        

    @property
    def level(self) -> dict:
        return self.__level

    @level.setter
    def level(self, value: dict):
        self._property_changed('level')
        self.__level = value        

    @property
    def mnav(self) -> dict:
        return self.__mnav

    @mnav.setter
    def mnav(self, value: dict):
        self._property_changed('mnav')
        self.__mnav = value        

    @property
    def es_momentum_score(self) -> dict:
        return self.__es_momentum_score

    @es_momentum_score.setter
    def es_momentum_score(self, value: dict):
        self._property_changed('es_momentum_score')
        self.__es_momentum_score = value        

    @property
    def curr_yield7_day(self) -> dict:
        return self.__curr_yield7_day

    @curr_yield7_day.setter
    def curr_yield7_day(self, value: dict):
        self._property_changed('curr_yield7_day')
        self.__curr_yield7_day = value        

    @property
    def pressure(self) -> dict:
        return self.__pressure

    @pressure.setter
    def pressure(self, value: dict):
        self._property_changed('pressure')
        self.__pressure = value        

    @property
    def short_description(self) -> dict:
        return self.__short_description

    @short_description.setter
    def short_description(self, value: dict):
        self._property_changed('short_description')
        self.__short_description = value        

    @property
    def feed(self) -> dict:
        return self.__feed

    @feed.setter
    def feed(self, value: dict):
        self._property_changed('feed')
        self.__feed = value        

    @property
    def net_weight(self) -> dict:
        return self.__net_weight

    @net_weight.setter
    def net_weight(self, value: dict):
        self._property_changed('net_weight')
        self.__net_weight = value        

    @property
    def portfolio_managers(self) -> dict:
        return self.__portfolio_managers

    @portfolio_managers.setter
    def portfolio_managers(self, value: dict):
        self._property_changed('portfolio_managers')
        self.__portfolio_managers = value        

    @property
    def asset_parameters_commodity_sector(self) -> dict:
        return self.__asset_parameters_commodity_sector

    @asset_parameters_commodity_sector.setter
    def asset_parameters_commodity_sector(self, value: dict):
        self._property_changed('asset_parameters_commodity_sector')
        self.__asset_parameters_commodity_sector = value        

    @property
    def bos_in_ticks(self) -> dict:
        return self.__bos_in_ticks

    @bos_in_ticks.setter
    def bos_in_ticks(self, value: dict):
        self._property_changed('bos_in_ticks')
        self.__bos_in_ticks = value        

    @property
    def price_notation2(self) -> dict:
        return self.__price_notation2

    @price_notation2.setter
    def price_notation2(self, value: dict):
        self._property_changed('price_notation2')
        self.__price_notation2 = value        

    @property
    def market_buffer_threshold(self) -> dict:
        return self.__market_buffer_threshold

    @market_buffer_threshold.setter
    def market_buffer_threshold(self, value: dict):
        self._property_changed('market_buffer_threshold')
        self.__market_buffer_threshold = value        

    @property
    def price_notation3(self) -> dict:
        return self.__price_notation3

    @price_notation3.setter
    def price_notation3(self, value: dict):
        self._property_changed('price_notation3')
        self.__price_notation3 = value        

    @property
    def cap_floor_vol(self) -> dict:
        return self.__cap_floor_vol

    @cap_floor_vol.setter
    def cap_floor_vol(self, value: dict):
        self._property_changed('cap_floor_vol')
        self.__cap_floor_vol = value        

    @property
    def submitter(self) -> dict:
        return self.__submitter

    @submitter.setter
    def submitter(self, value: dict):
        self._property_changed('submitter')
        self.__submitter = value        

    @property
    def notional(self) -> dict:
        return self.__notional

    @notional.setter
    def notional(self, value: dict):
        self._property_changed('notional')
        self.__notional = value        

    @property
    def es_disclosure_percentage(self) -> dict:
        return self.__es_disclosure_percentage

    @es_disclosure_percentage.setter
    def es_disclosure_percentage(self, value: dict):
        self._property_changed('es_disclosure_percentage')
        self.__es_disclosure_percentage = value        

    @property
    def investment_income(self) -> dict:
        return self.__investment_income

    @investment_income.setter
    def investment_income(self, value: dict):
        self._property_changed('investment_income')
        self.__investment_income = value        

    @property
    def forward_point_imm(self) -> dict:
        return self.__forward_point_imm

    @forward_point_imm.setter
    def forward_point_imm(self, value: dict):
        self._property_changed('forward_point_imm')
        self.__forward_point_imm = value        

    @property
    def client_short_name(self) -> dict:
        return self.__client_short_name

    @client_short_name.setter
    def client_short_name(self, value: dict):
        self._property_changed('client_short_name')
        self.__client_short_name = value        

    @property
    def group_category(self) -> dict:
        return self.__group_category

    @group_category.setter
    def group_category(self, value: dict):
        self._property_changed('group_category')
        self.__group_category = value        

    @property
    def bid_plus_ask(self) -> dict:
        return self.__bid_plus_ask

    @bid_plus_ask.setter
    def bid_plus_ask(self, value: dict):
        self._property_changed('bid_plus_ask')
        self.__bid_plus_ask = value        

    @property
    def foreign_ccy_rate(self) -> dict:
        return self.__foreign_ccy_rate

    @foreign_ccy_rate.setter
    def foreign_ccy_rate(self, value: dict):
        self._property_changed('foreign_ccy_rate')
        self.__foreign_ccy_rate = value        

    @property
    def election_odds(self) -> dict:
        return self.__election_odds

    @election_odds.setter
    def election_odds(self, value: dict):
        self._property_changed('election_odds')
        self.__election_odds = value        

    @property
    def require_anon_client_name(self) -> dict:
        return self.__require_anon_client_name

    @require_anon_client_name.setter
    def require_anon_client_name(self, value: dict):
        self._property_changed('require_anon_client_name')
        self.__require_anon_client_name = value        

    @property
    def total(self) -> dict:
        return self.__total

    @total.setter
    def total(self, value: dict):
        self._property_changed('total')
        self.__total = value        

    @property
    def asset_id(self) -> dict:
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: dict):
        self._property_changed('asset_id')
        self.__asset_id = value        

    @property
    def mkt_type(self) -> dict:
        return self.__mkt_type

    @mkt_type.setter
    def mkt_type(self, value: dict):
        self._property_changed('mkt_type')
        self.__mkt_type = value        

    @property
    def pricing_location(self) -> dict:
        return self.__pricing_location

    @pricing_location.setter
    def pricing_location(self, value: dict):
        self._property_changed('pricing_location')
        self.__pricing_location = value        

    @property
    def yield30_day(self) -> dict:
        return self.__yield30_day

    @yield30_day.setter
    def yield30_day(self, value: dict):
        self._property_changed('yield30_day')
        self.__yield30_day = value        

    @property
    def proportion_of_risk(self) -> dict:
        return self.__proportion_of_risk

    @proportion_of_risk.setter
    def proportion_of_risk(self, value: dict):
        self._property_changed('proportion_of_risk')
        self.__proportion_of_risk = value        

    @property
    def beta(self) -> dict:
        return self.__beta

    @beta.setter
    def beta(self, value: dict):
        self._property_changed('beta')
        self.__beta = value        

    @property
    def long_exposure(self) -> dict:
        return self.__long_exposure

    @long_exposure.setter
    def long_exposure(self, value: dict):
        self._property_changed('long_exposure')
        self.__long_exposure = value        

    @property
    def tcm_cost_participation_rate20_pct(self) -> dict:
        return self.__tcm_cost_participation_rate20_pct

    @tcm_cost_participation_rate20_pct.setter
    def tcm_cost_participation_rate20_pct(self, value: dict):
        self._property_changed('tcm_cost_participation_rate20_pct')
        self.__tcm_cost_participation_rate20_pct = value        

    @property
    def multi_asset_class_swap(self) -> dict:
        return self.__multi_asset_class_swap

    @multi_asset_class_swap.setter
    def multi_asset_class_swap(self, value: dict):
        self._property_changed('multi_asset_class_swap')
        self.__multi_asset_class_swap = value        

    @property
    def cross(self) -> dict:
        return self.__cross

    @cross.setter
    def cross(self, value: dict):
        self._property_changed('cross')
        self.__cross = value        

    @property
    def idea_status(self) -> dict:
        return self.__idea_status

    @idea_status.setter
    def idea_status(self, value: dict):
        self._property_changed('idea_status')
        self.__idea_status = value        

    @property
    def contract_subtype(self) -> dict:
        return self.__contract_subtype

    @contract_subtype.setter
    def contract_subtype(self, value: dict):
        self._property_changed('contract_subtype')
        self.__contract_subtype = value        

    @property
    def fx_forecast(self) -> dict:
        return self.__fx_forecast

    @fx_forecast.setter
    def fx_forecast(self, value: dict):
        self._property_changed('fx_forecast')
        self.__fx_forecast = value        

    @property
    def fixing_time_label(self) -> dict:
        return self.__fixing_time_label

    @fixing_time_label.setter
    def fixing_time_label(self, value: dict):
        self._property_changed('fixing_time_label')
        self.__fixing_time_label = value        

    @property
    def implementation_id(self) -> dict:
        return self.__implementation_id

    @implementation_id.setter
    def implementation_id(self, value: dict):
        self._property_changed('implementation_id')
        self.__implementation_id = value        

    @property
    def fill_id(self) -> dict:
        return self.__fill_id

    @fill_id.setter
    def fill_id(self, value: dict):
        self._property_changed('fill_id')
        self.__fill_id = value        

    @property
    def excess_returns(self) -> dict:
        return self.__excess_returns

    @excess_returns.setter
    def excess_returns(self, value: dict):
        self._property_changed('excess_returns')
        self.__excess_returns = value        

    @property
    def dollar_return(self) -> dict:
        return self.__dollar_return

    @dollar_return.setter
    def dollar_return(self, value: dict):
        self._property_changed('dollar_return')
        self.__dollar_return = value        

    @property
    def es_numeric_score(self) -> dict:
        return self.__es_numeric_score

    @es_numeric_score.setter
    def es_numeric_score(self, value: dict):
        self._property_changed('es_numeric_score')
        self.__es_numeric_score = value        

    @property
    def in_benchmark(self) -> dict:
        return self.__in_benchmark

    @in_benchmark.setter
    def in_benchmark(self, value: dict):
        self._property_changed('in_benchmark')
        self.__in_benchmark = value        

    @property
    def return_on_equity(self) -> dict:
        return self.__return_on_equity

    @return_on_equity.setter
    def return_on_equity(self, value: dict):
        self._property_changed('return_on_equity')
        self.__return_on_equity = value        

    @property
    def action_sdr(self) -> dict:
        return self.__action_sdr

    @action_sdr.setter
    def action_sdr(self, value: dict):
        self._property_changed('action_sdr')
        self.__action_sdr = value        

    @property
    def queue_in_lots_description(self) -> dict:
        return self.__queue_in_lots_description

    @queue_in_lots_description.setter
    def queue_in_lots_description(self, value: dict):
        self._property_changed('queue_in_lots_description')
        self.__queue_in_lots_description = value        

    @property
    def objective(self) -> dict:
        return self.__objective

    @objective.setter
    def objective(self, value: dict):
        self._property_changed('objective')
        self.__objective = value        

    @property
    def nav_price(self) -> dict:
        return self.__nav_price

    @nav_price.setter
    def nav_price(self, value: dict):
        self._property_changed('nav_price')
        self.__nav_price = value        

    @property
    def precipitation(self) -> dict:
        return self.__precipitation

    @precipitation.setter
    def precipitation(self, value: dict):
        self._property_changed('precipitation')
        self.__precipitation = value        

    @property
    def hedge_notional(self) -> dict:
        return self.__hedge_notional

    @hedge_notional.setter
    def hedge_notional(self, value: dict):
        self._property_changed('hedge_notional')
        self.__hedge_notional = value        

    @property
    def ask_low(self) -> dict:
        return self.__ask_low

    @ask_low.setter
    def ask_low(self, value: dict):
        self._property_changed('ask_low')
        self.__ask_low = value        

    @property
    def beta_adjusted_net_exposure(self) -> dict:
        return self.__beta_adjusted_net_exposure

    @beta_adjusted_net_exposure.setter
    def beta_adjusted_net_exposure(self, value: dict):
        self._property_changed('beta_adjusted_net_exposure')
        self.__beta_adjusted_net_exposure = value        

    @property
    def expiry(self) -> dict:
        return self.__expiry

    @expiry.setter
    def expiry(self, value: dict):
        self._property_changed('expiry')
        self.__expiry = value        

    @property
    def avg_monthly_yield(self) -> dict:
        return self.__avg_monthly_yield

    @avg_monthly_yield.setter
    def avg_monthly_yield(self, value: dict):
        self._property_changed('avg_monthly_yield')
        self.__avg_monthly_yield = value        

    @property
    def period_direction(self) -> dict:
        return self.__period_direction

    @period_direction.setter
    def period_direction(self, value: dict):
        self._property_changed('period_direction')
        self.__period_direction = value        

    @property
    def earnings_per_share(self) -> dict:
        return self.__earnings_per_share

    @earnings_per_share.setter
    def earnings_per_share(self, value: dict):
        self._property_changed('earnings_per_share')
        self.__earnings_per_share = value        

    @property
    def strike_percentage(self) -> dict:
        return self.__strike_percentage

    @strike_percentage.setter
    def strike_percentage(self, value: dict):
        self._property_changed('strike_percentage')
        self.__strike_percentage = value        

    @property
    def excess_return_price(self) -> dict:
        return self.__excess_return_price

    @excess_return_price.setter
    def excess_return_price(self, value: dict):
        self._property_changed('excess_return_price')
        self.__excess_return_price = value        

    @property
    def prev_close_bid(self) -> dict:
        return self.__prev_close_bid

    @prev_close_bid.setter
    def prev_close_bid(self, value: dict):
        self._property_changed('prev_close_bid')
        self.__prev_close_bid = value        

    @property
    def fx_pnl(self) -> dict:
        return self.__fx_pnl

    @fx_pnl.setter
    def fx_pnl(self, value: dict):
        self._property_changed('fx_pnl')
        self.__fx_pnl = value        

    @property
    def tcm_cost_horizon16_day(self) -> dict:
        return self.__tcm_cost_horizon16_day

    @tcm_cost_horizon16_day.setter
    def tcm_cost_horizon16_day(self, value: dict):
        self._property_changed('tcm_cost_horizon16_day')
        self.__tcm_cost_horizon16_day = value        

    @property
    def sales_per_share(self) -> dict:
        return self.__sales_per_share

    @sales_per_share.setter
    def sales_per_share(self, value: dict):
        self._property_changed('sales_per_share')
        self.__sales_per_share = value        

    @property
    def asset_classifications_gics_industry_group(self) -> dict:
        return self.__asset_classifications_gics_industry_group

    @asset_classifications_gics_industry_group.setter
    def asset_classifications_gics_industry_group(self, value: dict):
        self._property_changed('asset_classifications_gics_industry_group')
        self.__asset_classifications_gics_industry_group = value        

    @property
    def unadjusted_close(self) -> dict:
        return self.__unadjusted_close

    @unadjusted_close.setter
    def unadjusted_close(self, value: dict):
        self._property_changed('unadjusted_close')
        self.__unadjusted_close = value        

    @property
    def lending_sec_id(self) -> dict:
        return self.__lending_sec_id

    @lending_sec_id.setter
    def lending_sec_id(self, value: dict):
        self._property_changed('lending_sec_id')
        self.__lending_sec_id = value        

    @property
    def equity_theta(self) -> dict:
        return self.__equity_theta

    @equity_theta.setter
    def equity_theta(self, value: dict):
        self._property_changed('equity_theta')
        self.__equity_theta = value        

    @property
    def execution_fee(self) -> dict:
        return self.__execution_fee

    @execution_fee.setter
    def execution_fee(self, value: dict):
        self._property_changed('execution_fee')
        self.__execution_fee = value        

    @property
    def collateral_percentage_actual(self) -> dict:
        return self.__collateral_percentage_actual

    @collateral_percentage_actual.setter
    def collateral_percentage_actual(self, value: dict):
        self._property_changed('collateral_percentage_actual')
        self.__collateral_percentage_actual = value        

    @property
    def mixed_swap(self) -> dict:
        return self.__mixed_swap

    @mixed_swap.setter
    def mixed_swap(self, value: dict):
        self._property_changed('mixed_swap')
        self.__mixed_swap = value        

    @property
    def snowfall(self) -> dict:
        return self.__snowfall

    @snowfall.setter
    def snowfall(self, value: dict):
        self._property_changed('snowfall')
        self.__snowfall = value        

    @property
    def mic(self) -> dict:
        return self.__mic

    @mic.setter
    def mic(self, value: dict):
        self._property_changed('mic')
        self.__mic = value        

    @property
    def mid(self) -> dict:
        return self.__mid

    @mid.setter
    def mid(self, value: dict):
        self._property_changed('mid')
        self.__mid = value        

    @property
    def auto_exec_state(self) -> dict:
        return self.__auto_exec_state

    @auto_exec_state.setter
    def auto_exec_state(self, value: dict):
        self._property_changed('auto_exec_state')
        self.__auto_exec_state = value        

    @property
    def relative_return_ytd(self) -> dict:
        return self.__relative_return_ytd

    @relative_return_ytd.setter
    def relative_return_ytd(self, value: dict):
        self._property_changed('relative_return_ytd')
        self.__relative_return_ytd = value        

    @property
    def long(self) -> dict:
        return self.__long

    @long.setter
    def long(self, value: dict):
        self._property_changed('long')
        self.__long = value        

    @property
    def region_code(self) -> dict:
        return self.__region_code

    @region_code.setter
    def region_code(self, value: dict):
        self._property_changed('region_code')
        self.__region_code = value        

    @property
    def long_weight(self) -> dict:
        return self.__long_weight

    @long_weight.setter
    def long_weight(self, value: dict):
        self._property_changed('long_weight')
        self.__long_weight = value        

    @property
    def calculation_time(self) -> dict:
        return self.__calculation_time

    @calculation_time.setter
    def calculation_time(self, value: dict):
        self._property_changed('calculation_time')
        self.__calculation_time = value        

    @property
    def real_time_restriction_status(self) -> dict:
        return self.__real_time_restriction_status

    @real_time_restriction_status.setter
    def real_time_restriction_status(self, value: dict):
        self._property_changed('real_time_restriction_status')
        self.__real_time_restriction_status = value        

    @property
    def average_realized_variance(self) -> dict:
        return self.__average_realized_variance

    @average_realized_variance.setter
    def average_realized_variance(self, value: dict):
        self._property_changed('average_realized_variance')
        self.__average_realized_variance = value        

    @property
    def financial_returns_score(self) -> dict:
        return self.__financial_returns_score

    @financial_returns_score.setter
    def financial_returns_score(self, value: dict):
        self._property_changed('financial_returns_score')
        self.__financial_returns_score = value        

    @property
    def year_or_quarter(self) -> dict:
        return self.__year_or_quarter

    @year_or_quarter.setter
    def year_or_quarter(self, value: dict):
        self._property_changed('year_or_quarter')
        self.__year_or_quarter = value        

    @property
    def settlement_type(self) -> dict:
        return self.__settlement_type

    @settlement_type.setter
    def settlement_type(self, value: dict):
        self._property_changed('settlement_type')
        self.__settlement_type = value        

    @property
    def net_change(self) -> dict:
        return self.__net_change

    @net_change.setter
    def net_change(self, value: dict):
        self._property_changed('net_change')
        self.__net_change = value        

    @property
    def non_symbol_dimensions(self) -> dict:
        return self.__non_symbol_dimensions

    @non_symbol_dimensions.setter
    def non_symbol_dimensions(self, value: dict):
        self._property_changed('non_symbol_dimensions')
        self.__non_symbol_dimensions = value        

    @property
    def leg_two_fixed_payment_currency(self) -> dict:
        return self.__leg_two_fixed_payment_currency

    @leg_two_fixed_payment_currency.setter
    def leg_two_fixed_payment_currency(self, value: dict):
        self._property_changed('leg_two_fixed_payment_currency')
        self.__leg_two_fixed_payment_currency = value        

    @property
    def number_of_underliers(self) -> dict:
        return self.__number_of_underliers

    @number_of_underliers.setter
    def number_of_underliers(self, value: dict):
        self._property_changed('number_of_underliers')
        self.__number_of_underliers = value        

    @property
    def swap_type(self) -> dict:
        return self.__swap_type

    @swap_type.setter
    def swap_type(self, value: dict):
        self._property_changed('swap_type')
        self.__swap_type = value        

    @property
    def forecast_type(self) -> dict:
        return self.__forecast_type

    @forecast_type.setter
    def forecast_type(self, value: dict):
        self._property_changed('forecast_type')
        self.__forecast_type = value        

    @property
    def asset_classifications_country_name(self) -> dict:
        return self.__asset_classifications_country_name

    @asset_classifications_country_name.setter
    def asset_classifications_country_name(self, value: dict):
        self._property_changed('asset_classifications_country_name')
        self.__asset_classifications_country_name = value        

    @property
    def new_ideas_ytd(self) -> dict:
        return self.__new_ideas_ytd

    @new_ideas_ytd.setter
    def new_ideas_ytd(self, value: dict):
        self._property_changed('new_ideas_ytd')
        self.__new_ideas_ytd = value        

    @property
    def management_fee(self) -> dict:
        return self.__management_fee

    @management_fee.setter
    def management_fee(self, value: dict):
        self._property_changed('management_fee')
        self.__management_fee = value        

    @property
    def open(self) -> dict:
        return self.__open

    @open.setter
    def open(self, value: dict):
        self._property_changed('open')
        self.__open = value        

    @property
    def source_id(self) -> dict:
        return self.__source_id

    @source_id.setter
    def source_id(self, value: dict):
        self._property_changed('source_id')
        self.__source_id = value        

    @property
    def country(self) -> dict:
        return self.__country

    @country.setter
    def country(self, value: dict):
        self._property_changed('country')
        self.__country = value        

    @property
    def cusip(self) -> dict:
        return self.__cusip

    @cusip.setter
    def cusip(self, value: dict):
        self._property_changed('cusip')
        self.__cusip = value        

    @property
    def touch_spread_score(self) -> dict:
        return self.__touch_spread_score

    @touch_spread_score.setter
    def touch_spread_score(self, value: dict):
        self._property_changed('touch_spread_score')
        self.__touch_spread_score = value        

    @property
    def spread_option_atm_fwd_rate(self) -> dict:
        return self.__spread_option_atm_fwd_rate

    @spread_option_atm_fwd_rate.setter
    def spread_option_atm_fwd_rate(self, value: dict):
        self._property_changed('spread_option_atm_fwd_rate')
        self.__spread_option_atm_fwd_rate = value        

    @property
    def net_exposure(self) -> dict:
        return self.__net_exposure

    @net_exposure.setter
    def net_exposure(self, value: dict):
        self._property_changed('net_exposure')
        self.__net_exposure = value        

    @property
    def frequency(self) -> dict:
        return self.__frequency

    @frequency.setter
    def frequency(self, value: dict):
        self._property_changed('frequency')
        self.__frequency = value        

    @property
    def activity_id(self) -> dict:
        return self.__activity_id

    @activity_id.setter
    def activity_id(self, value: dict):
        self._property_changed('activity_id')
        self.__activity_id = value        

    @property
    def estimated_impact(self) -> dict:
        return self.__estimated_impact

    @estimated_impact.setter
    def estimated_impact(self, value: dict):
        self._property_changed('estimated_impact')
        self.__estimated_impact = value        

    @property
    def loan_spread_bucket(self) -> dict:
        return self.__loan_spread_bucket

    @loan_spread_bucket.setter
    def loan_spread_bucket(self, value: dict):
        self._property_changed('loan_spread_bucket')
        self.__loan_spread_bucket = value        

    @property
    def asset_parameters_pricing_location(self) -> dict:
        return self.__asset_parameters_pricing_location

    @asset_parameters_pricing_location.setter
    def asset_parameters_pricing_location(self, value: dict):
        self._property_changed('asset_parameters_pricing_location')
        self.__asset_parameters_pricing_location = value        

    @property
    def event_description(self) -> dict:
        return self.__event_description

    @event_description.setter
    def event_description(self, value: dict):
        self._property_changed('event_description')
        self.__event_description = value        

    @property
    def provide_non_display_tape_a(self) -> dict:
        return self.__provide_non_display_tape_a

    @provide_non_display_tape_a.setter
    def provide_non_display_tape_a(self, value: dict):
        self._property_changed('provide_non_display_tape_a')
        self.__provide_non_display_tape_a = value        

    @property
    def strike_reference(self) -> dict:
        return self.__strike_reference

    @strike_reference.setter
    def strike_reference(self, value: dict):
        self._property_changed('strike_reference')
        self.__strike_reference = value        

    @property
    def details(self) -> dict:
        return self.__details

    @details.setter
    def details(self, value: dict):
        self._property_changed('details')
        self.__details = value        

    @property
    def provide_non_display_tape_c(self) -> dict:
        return self.__provide_non_display_tape_c

    @provide_non_display_tape_c.setter
    def provide_non_display_tape_c(self, value: dict):
        self._property_changed('provide_non_display_tape_c')
        self.__provide_non_display_tape_c = value        

    @property
    def asset_count(self) -> dict:
        return self.__asset_count

    @asset_count.setter
    def asset_count(self, value: dict):
        self._property_changed('asset_count')
        self.__asset_count = value        

    @property
    def provide_non_display_tape_b(self) -> dict:
        return self.__provide_non_display_tape_b

    @provide_non_display_tape_b.setter
    def provide_non_display_tape_b(self, value: dict):
        self._property_changed('provide_non_display_tape_b')
        self.__provide_non_display_tape_b = value        

    @property
    def sector(self) -> dict:
        return self.__sector

    @sector.setter
    def sector(self, value: dict):
        self._property_changed('sector')
        self.__sector = value        

    @property
    def fundamental_metric(self) -> dict:
        return self.__fundamental_metric

    @fundamental_metric.setter
    def fundamental_metric(self, value: dict):
        self._property_changed('fundamental_metric')
        self.__fundamental_metric = value        

    @property
    def absolute_value(self) -> dict:
        return self.__absolute_value

    @absolute_value.setter
    def absolute_value(self, value: dict):
        self._property_changed('absolute_value')
        self.__absolute_value = value        

    @property
    def closing_report(self) -> dict:
        return self.__closing_report

    @closing_report.setter
    def closing_report(self, value: dict):
        self._property_changed('closing_report')
        self.__closing_report = value        

    @property
    def long_tenor(self) -> dict:
        return self.__long_tenor

    @long_tenor.setter
    def long_tenor(self, value: dict):
        self._property_changed('long_tenor')
        self.__long_tenor = value        

    @property
    def mctr(self) -> dict:
        return self.__mctr

    @mctr.setter
    def mctr(self, value: dict):
        self._property_changed('mctr')
        self.__mctr = value        

    @property
    def historical_close(self) -> dict:
        return self.__historical_close

    @historical_close.setter
    def historical_close(self, value: dict):
        self._property_changed('historical_close')
        self.__historical_close = value        

    @property
    def asset_count_priced(self) -> dict:
        return self.__asset_count_priced

    @asset_count_priced.setter
    def asset_count_priced(self, value: dict):
        self._property_changed('asset_count_priced')
        self.__asset_count_priced = value        

    @property
    def idea_id(self) -> dict:
        return self.__idea_id

    @idea_id.setter
    def idea_id(self, value: dict):
        self._property_changed('idea_id')
        self.__idea_id = value        

    @property
    def comment_status(self) -> dict:
        return self.__comment_status

    @comment_status.setter
    def comment_status(self, value: dict):
        self._property_changed('comment_status')
        self.__comment_status = value        

    @property
    def marginal_cost(self) -> dict:
        return self.__marginal_cost

    @marginal_cost.setter
    def marginal_cost(self, value: dict):
        self._property_changed('marginal_cost')
        self.__marginal_cost = value        

    @property
    def settlement_currency(self) -> dict:
        return self.__settlement_currency

    @settlement_currency.setter
    def settlement_currency(self, value: dict):
        self._property_changed('settlement_currency')
        self.__settlement_currency = value        

    @property
    def client_weight(self) -> dict:
        return self.__client_weight

    @client_weight.setter
    def client_weight(self, value: dict):
        self._property_changed('client_weight')
        self.__client_weight = value        

    @property
    def indication_of_collateralization(self) -> dict:
        return self.__indication_of_collateralization

    @indication_of_collateralization.setter
    def indication_of_collateralization(self, value: dict):
        self._property_changed('indication_of_collateralization')
        self.__indication_of_collateralization = value        

    @property
    def liq_wkly(self) -> dict:
        return self.__liq_wkly

    @liq_wkly.setter
    def liq_wkly(self, value: dict):
        self._property_changed('liq_wkly')
        self.__liq_wkly = value        

    @property
    def lending_partner_fee(self) -> dict:
        return self.__lending_partner_fee

    @lending_partner_fee.setter
    def lending_partner_fee(self, value: dict):
        self._property_changed('lending_partner_fee')
        self.__lending_partner_fee = value        

    @property
    def region(self) -> dict:
        return self.__region

    @region.setter
    def region(self, value: dict):
        self._property_changed('region')
        self.__region = value        

    @property
    def tenor2(self) -> dict:
        return self.__tenor2

    @tenor2.setter
    def tenor2(self, value: dict):
        self._property_changed('tenor2')
        self.__tenor2 = value        

    @property
    def option_premium(self) -> dict:
        return self.__option_premium

    @option_premium.setter
    def option_premium(self, value: dict):
        self._property_changed('option_premium')
        self.__option_premium = value        

    @property
    def owner_name(self) -> dict:
        return self.__owner_name

    @owner_name.setter
    def owner_name(self, value: dict):
        self._property_changed('owner_name')
        self.__owner_name = value        

    @property
    def last_updated_by_id(self) -> dict:
        return self.__last_updated_by_id

    @last_updated_by_id.setter
    def last_updated_by_id(self, value: dict):
        self._property_changed('last_updated_by_id')
        self.__last_updated_by_id = value        

    @property
    def z_score(self) -> dict:
        return self.__z_score

    @z_score.setter
    def z_score(self, value: dict):
        self._property_changed('z_score')
        self.__z_score = value        

    @property
    def legal_entity_acct(self) -> dict:
        return self.__legal_entity_acct

    @legal_entity_acct.setter
    def legal_entity_acct(self, value: dict):
        self._property_changed('legal_entity_acct')
        self.__legal_entity_acct = value        

    @property
    def target_shareholder_meeting_date(self) -> dict:
        return self.__target_shareholder_meeting_date

    @target_shareholder_meeting_date.setter
    def target_shareholder_meeting_date(self, value: dict):
        self._property_changed('target_shareholder_meeting_date')
        self.__target_shareholder_meeting_date = value        

    @property
    def event_start_time(self) -> dict:
        return self.__event_start_time

    @event_start_time.setter
    def event_start_time(self, value: dict):
        self._property_changed('event_start_time')
        self.__event_start_time = value        

    @property
    def turnover(self) -> dict:
        return self.__turnover

    @turnover.setter
    def turnover(self, value: dict):
        self._property_changed('turnover')
        self.__turnover = value        

    @property
    def price_spot_target_unit(self) -> dict:
        return self.__price_spot_target_unit

    @price_spot_target_unit.setter
    def price_spot_target_unit(self, value: dict):
        self._property_changed('price_spot_target_unit')
        self.__price_spot_target_unit = value        

    @property
    def leg_one_type(self) -> dict:
        return self.__leg_one_type

    @leg_one_type.setter
    def leg_one_type(self, value: dict):
        self._property_changed('leg_one_type')
        self.__leg_one_type = value        

    @property
    def leg_two_spread(self) -> dict:
        return self.__leg_two_spread

    @leg_two_spread.setter
    def leg_two_spread(self, value: dict):
        self._property_changed('leg_two_spread')
        self.__leg_two_spread = value        

    @property
    def coverage(self) -> dict:
        return self.__coverage

    @coverage.setter
    def coverage(self, value: dict):
        self._property_changed('coverage')
        self.__coverage = value        

    @property
    def g_percentile(self) -> dict:
        return self.__g_percentile

    @g_percentile.setter
    def g_percentile(self, value: dict):
        self._property_changed('g_percentile')
        self.__g_percentile = value        

    @property
    def lending_fund_nav(self) -> dict:
        return self.__lending_fund_nav

    @lending_fund_nav.setter
    def lending_fund_nav(self, value: dict):
        self._property_changed('lending_fund_nav')
        self.__lending_fund_nav = value        

    @property
    def source_original_category(self) -> dict:
        return self.__source_original_category

    @source_original_category.setter
    def source_original_category(self, value: dict):
        self._property_changed('source_original_category')
        self.__source_original_category = value        

    @property
    def composite5_day_adv(self) -> dict:
        return self.__composite5_day_adv

    @composite5_day_adv.setter
    def composite5_day_adv(self, value: dict):
        self._property_changed('composite5_day_adv')
        self.__composite5_day_adv = value        

    @property
    def marginal_contribution_to_risk(self) -> dict:
        return self.__marginal_contribution_to_risk

    @marginal_contribution_to_risk.setter
    def marginal_contribution_to_risk(self, value: dict):
        self._property_changed('marginal_contribution_to_risk')
        self.__marginal_contribution_to_risk = value        

    @property
    def new_ideas_wtd(self) -> dict:
        return self.__new_ideas_wtd

    @new_ideas_wtd.setter
    def new_ideas_wtd(self, value: dict):
        self._property_changed('new_ideas_wtd')
        self.__new_ideas_wtd = value        

    @property
    def asset_class_sdr(self) -> dict:
        return self.__asset_class_sdr

    @asset_class_sdr.setter
    def asset_class_sdr(self, value: dict):
        self._property_changed('asset_class_sdr')
        self.__asset_class_sdr = value        

    @property
    def location(self) -> dict:
        return self.__location

    @location.setter
    def location(self, value: dict):
        self._property_changed('location')
        self.__location = value        

    @property
    def comment(self) -> dict:
        return self.__comment

    @comment.setter
    def comment(self, value: dict):
        self._property_changed('comment')
        self.__comment = value        

    @property
    def source_symbol(self) -> dict:
        return self.__source_symbol

    @source_symbol.setter
    def source_symbol(self, value: dict):
        self._property_changed('source_symbol')
        self.__source_symbol = value        

    @property
    def scenario_id(self) -> dict:
        return self.__scenario_id

    @scenario_id.setter
    def scenario_id(self, value: dict):
        self._property_changed('scenario_id')
        self.__scenario_id = value        

    @property
    def ask_unadjusted(self) -> dict:
        return self.__ask_unadjusted

    @ask_unadjusted.setter
    def ask_unadjusted(self, value: dict):
        self._property_changed('ask_unadjusted')
        self.__ask_unadjusted = value        

    @property
    def termination_tenor(self) -> dict:
        return self.__termination_tenor

    @termination_tenor.setter
    def termination_tenor(self, value: dict):
        self._property_changed('termination_tenor')
        self.__termination_tenor = value        

    @property
    def queue_clock_time(self) -> dict:
        return self.__queue_clock_time

    @queue_clock_time.setter
    def queue_clock_time(self, value: dict):
        self._property_changed('queue_clock_time')
        self.__queue_clock_time = value        

    @property
    def restrict_external_derived_data(self) -> dict:
        return self.__restrict_external_derived_data

    @restrict_external_derived_data.setter
    def restrict_external_derived_data(self, value: dict):
        self._property_changed('restrict_external_derived_data')
        self.__restrict_external_derived_data = value        

    @property
    def ask_change(self) -> dict:
        return self.__ask_change

    @ask_change.setter
    def ask_change(self, value: dict):
        self._property_changed('ask_change')
        self.__ask_change = value        

    @property
    def tcm_cost_participation_rate50_pct(self) -> dict:
        return self.__tcm_cost_participation_rate50_pct

    @tcm_cost_participation_rate50_pct.setter
    def tcm_cost_participation_rate50_pct(self, value: dict):
        self._property_changed('tcm_cost_participation_rate50_pct')
        self.__tcm_cost_participation_rate50_pct = value        

    @property
    def contract_type(self) -> dict:
        return self.__contract_type

    @contract_type.setter
    def contract_type(self, value: dict):
        self._property_changed('contract_type')
        self.__contract_type = value        

    @property
    def forward_price(self) -> dict:
        return self.__forward_price

    @forward_price.setter
    def forward_price(self, value: dict):
        self._property_changed('forward_price')
        self.__forward_price = value        

    @property
    def type(self) -> dict:
        return self.__type

    @type.setter
    def type(self, value: dict):
        self._property_changed('type')
        self.__type = value        

    @property
    def strike_ref(self) -> dict:
        return self.__strike_ref

    @strike_ref.setter
    def strike_ref(self, value: dict):
        self._property_changed('strike_ref')
        self.__strike_ref = value        

    @property
    def mdapi(self) -> dict:
        return self.__mdapi

    @mdapi.setter
    def mdapi(self, value: dict):
        self._property_changed('mdapi')
        self.__mdapi = value        

    @property
    def cumulative_pnl(self) -> dict:
        return self.__cumulative_pnl

    @cumulative_pnl.setter
    def cumulative_pnl(self, value: dict):
        self._property_changed('cumulative_pnl')
        self.__cumulative_pnl = value        

    @property
    def short_tenor(self) -> dict:
        return self.__short_tenor

    @short_tenor.setter
    def short_tenor(self, value: dict):
        self._property_changed('short_tenor')
        self.__short_tenor = value        

    @property
    def loss(self) -> dict:
        return self.__loss

    @loss.setter
    def loss(self, value: dict):
        self._property_changed('loss')
        self.__loss = value        

    @property
    def unadjusted_volume(self) -> dict:
        return self.__unadjusted_volume

    @unadjusted_volume.setter
    def unadjusted_volume(self, value: dict):
        self._property_changed('unadjusted_volume')
        self.__unadjusted_volume = value        

    @property
    def midcurve_vol(self) -> dict:
        return self.__midcurve_vol

    @midcurve_vol.setter
    def midcurve_vol(self, value: dict):
        self._property_changed('midcurve_vol')
        self.__midcurve_vol = value        

    @property
    def trading_cost_pnl(self) -> dict:
        return self.__trading_cost_pnl

    @trading_cost_pnl.setter
    def trading_cost_pnl(self, value: dict):
        self._property_changed('trading_cost_pnl')
        self.__trading_cost_pnl = value        

    @property
    def price_notation_type(self) -> dict:
        return self.__price_notation_type

    @price_notation_type.setter
    def price_notation_type(self, value: dict):
        self._property_changed('price_notation_type')
        self.__price_notation_type = value        

    @property
    def price(self) -> dict:
        return self.__price

    @price.setter
    def price(self, value: dict):
        self._property_changed('price')
        self.__price = value        

    @property
    def payment_quantity(self) -> dict:
        return self.__payment_quantity

    @payment_quantity.setter
    def payment_quantity(self, value: dict):
        self._property_changed('payment_quantity')
        self.__payment_quantity = value        

    @property
    def position_idx(self) -> dict:
        return self.__position_idx

    @position_idx.setter
    def position_idx(self, value: dict):
        self._property_changed('position_idx')
        self.__position_idx = value        

    @property
    def sec_name(self) -> dict:
        return self.__sec_name

    @sec_name.setter
    def sec_name(self, value: dict):
        self._property_changed('sec_name')
        self.__sec_name = value        

    @property
    def implied_volatility_by_relative_strike(self) -> dict:
        return self.__implied_volatility_by_relative_strike

    @implied_volatility_by_relative_strike.setter
    def implied_volatility_by_relative_strike(self, value: dict):
        self._property_changed('implied_volatility_by_relative_strike')
        self.__implied_volatility_by_relative_strike = value        

    @property
    def percent_adv(self) -> dict:
        return self.__percent_adv

    @percent_adv.setter
    def percent_adv(self, value: dict):
        self._property_changed('percent_adv')
        self.__percent_adv = value        

    @property
    def sub_region(self) -> dict:
        return self.__sub_region

    @sub_region.setter
    def sub_region(self, value: dict):
        self._property_changed('sub_region')
        self.__sub_region = value        

    @property
    def contract(self) -> dict:
        return self.__contract

    @contract.setter
    def contract(self, value: dict):
        self._property_changed('contract')
        self.__contract = value        

    @property
    def payment_frequency1(self) -> dict:
        return self.__payment_frequency1

    @payment_frequency1.setter
    def payment_frequency1(self, value: dict):
        self._property_changed('payment_frequency1')
        self.__payment_frequency1 = value        

    @property
    def payment_frequency2(self) -> dict:
        return self.__payment_frequency2

    @payment_frequency2.setter
    def payment_frequency2(self, value: dict):
        self._property_changed('payment_frequency2')
        self.__payment_frequency2 = value        

    @property
    def bespoke(self) -> dict:
        return self.__bespoke

    @bespoke.setter
    def bespoke(self, value: dict):
        self._property_changed('bespoke')
        self.__bespoke = value        

    @property
    def repo_tenor(self) -> dict:
        return self.__repo_tenor

    @repo_tenor.setter
    def repo_tenor(self, value: dict):
        self._property_changed('repo_tenor')
        self.__repo_tenor = value        

    @property
    def quality_stars(self) -> dict:
        return self.__quality_stars

    @quality_stars.setter
    def quality_stars(self, value: dict):
        self._property_changed('quality_stars')
        self.__quality_stars = value        

    @property
    def source_ticker(self) -> dict:
        return self.__source_ticker

    @source_ticker.setter
    def source_ticker(self, value: dict):
        self._property_changed('source_ticker')
        self.__source_ticker = value        

    @property
    def gsid(self) -> dict:
        return self.__gsid

    @gsid.setter
    def gsid(self, value: dict):
        self._property_changed('gsid')
        self.__gsid = value        

    @property
    def lending_fund(self) -> dict:
        return self.__lending_fund

    @lending_fund.setter
    def lending_fund(self, value: dict):
        self._property_changed('lending_fund')
        self.__lending_fund = value        

    @property
    def tcm_cost_participation_rate15_pct(self) -> dict:
        return self.__tcm_cost_participation_rate15_pct

    @tcm_cost_participation_rate15_pct.setter
    def tcm_cost_participation_rate15_pct(self, value: dict):
        self._property_changed('tcm_cost_participation_rate15_pct')
        self.__tcm_cost_participation_rate15_pct = value        

    @property
    def sensitivity(self) -> dict:
        return self.__sensitivity

    @sensitivity.setter
    def sensitivity(self, value: dict):
        self._property_changed('sensitivity')
        self.__sensitivity = value        

    @property
    def fiscal_year(self) -> dict:
        return self.__fiscal_year

    @fiscal_year.setter
    def fiscal_year(self, value: dict):
        self._property_changed('fiscal_year')
        self.__fiscal_year = value        

    @property
    def internal(self) -> dict:
        return self.__internal

    @internal.setter
    def internal(self, value: dict):
        self._property_changed('internal')
        self.__internal = value        

    @property
    def asset_classifications_gics_industry(self) -> dict:
        return self.__asset_classifications_gics_industry

    @asset_classifications_gics_industry.setter
    def asset_classifications_gics_industry(self, value: dict):
        self._property_changed('asset_classifications_gics_industry')
        self.__asset_classifications_gics_industry = value        

    @property
    def adjusted_bid_price(self) -> dict:
        return self.__adjusted_bid_price

    @adjusted_bid_price.setter
    def adjusted_bid_price(self, value: dict):
        self._property_changed('adjusted_bid_price')
        self.__adjusted_bid_price = value        

    @property
    def var_swap(self) -> dict:
        return self.__var_swap

    @var_swap.setter
    def var_swap(self, value: dict):
        self._property_changed('var_swap')
        self.__var_swap = value        

    @property
    def fixed_payment_leg2(self) -> dict:
        return self.__fixed_payment_leg2

    @fixed_payment_leg2.setter
    def fixed_payment_leg2(self, value: dict):
        self._property_changed('fixed_payment_leg2')
        self.__fixed_payment_leg2 = value        

    @property
    def fixed_payment_leg1(self) -> dict:
        return self.__fixed_payment_leg1

    @fixed_payment_leg1.setter
    def fixed_payment_leg1(self, value: dict):
        self._property_changed('fixed_payment_leg1')
        self.__fixed_payment_leg1 = value        

    @property
    def low_unadjusted(self) -> dict:
        return self.__low_unadjusted

    @low_unadjusted.setter
    def low_unadjusted(self, value: dict):
        self._property_changed('low_unadjusted')
        self.__low_unadjusted = value        

    @property
    def original_dissemination_id(self) -> dict:
        return self.__original_dissemination_id

    @original_dissemination_id.setter
    def original_dissemination_id(self, value: dict):
        self._property_changed('original_dissemination_id')
        self.__original_dissemination_id = value        

    @property
    def macs_secondary_asset_class(self) -> dict:
        return self.__macs_secondary_asset_class

    @macs_secondary_asset_class.setter
    def macs_secondary_asset_class(self, value: dict):
        self._property_changed('macs_secondary_asset_class')
        self.__macs_secondary_asset_class = value        

    @property
    def leg_two_averaging_method(self) -> dict:
        return self.__leg_two_averaging_method

    @leg_two_averaging_method.setter
    def leg_two_averaging_method(self, value: dict):
        self._property_changed('leg_two_averaging_method')
        self.__leg_two_averaging_method = value        

    @property
    def sectors_raw(self) -> dict:
        return self.__sectors_raw

    @sectors_raw.setter
    def sectors_raw(self, value: dict):
        self._property_changed('sectors_raw')
        self.__sectors_raw = value        

    @property
    def shareclass_price(self) -> dict:
        return self.__shareclass_price

    @shareclass_price.setter
    def shareclass_price(self, value: dict):
        self._property_changed('shareclass_price')
        self.__shareclass_price = value        

    @property
    def integrated_score(self) -> dict:
        return self.__integrated_score

    @integrated_score.setter
    def integrated_score(self, value: dict):
        self._property_changed('integrated_score')
        self.__integrated_score = value        

    @property
    def trade_size(self) -> dict:
        return self.__trade_size

    @trade_size.setter
    def trade_size(self, value: dict):
        self._property_changed('trade_size')
        self.__trade_size = value        

    @property
    def price_spot_entry_value(self) -> dict:
        return self.__price_spot_entry_value

    @price_spot_entry_value.setter
    def price_spot_entry_value(self, value: dict):
        self._property_changed('price_spot_entry_value')
        self.__price_spot_entry_value = value        

    @property
    def symbol_dimensions(self) -> dict:
        return self.__symbol_dimensions

    @symbol_dimensions.setter
    def symbol_dimensions(self, value: dict):
        self._property_changed('symbol_dimensions')
        self.__symbol_dimensions = value        

    @property
    def index_location_leg1(self) -> dict:
        return self.__index_location_leg1

    @index_location_leg1.setter
    def index_location_leg1(self, value: dict):
        self._property_changed('index_location_leg1')
        self.__index_location_leg1 = value        

    @property
    def index_location_leg2(self) -> dict:
        return self.__index_location_leg2

    @index_location_leg2.setter
    def index_location_leg2(self, value: dict):
        self._property_changed('index_location_leg2')
        self.__index_location_leg2 = value        

    @property
    def option_type_sdr(self) -> dict:
        return self.__option_type_sdr

    @option_type_sdr.setter
    def option_type_sdr(self, value: dict):
        self._property_changed('option_type_sdr')
        self.__option_type_sdr = value        

    @property
    def scenario_group_id(self) -> dict:
        return self.__scenario_group_id

    @scenario_group_id.setter
    def scenario_group_id(self, value: dict):
        self._property_changed('scenario_group_id')
        self.__scenario_group_id = value        

    @property
    def avg_yield7_day(self) -> dict:
        return self.__avg_yield7_day

    @avg_yield7_day.setter
    def avg_yield7_day(self, value: dict):
        self._property_changed('avg_yield7_day')
        self.__avg_yield7_day = value        

    @property
    def average_implied_variance(self) -> dict:
        return self.__average_implied_variance

    @average_implied_variance.setter
    def average_implied_variance(self, value: dict):
        self._property_changed('average_implied_variance')
        self.__average_implied_variance = value        

    @property
    def averaging_method_leg2(self) -> dict:
        return self.__averaging_method_leg2

    @averaging_method_leg2.setter
    def averaging_method_leg2(self, value: dict):
        self._property_changed('averaging_method_leg2')
        self.__averaging_method_leg2 = value        

    @property
    def avg_trade_rate_description(self) -> dict:
        return self.__avg_trade_rate_description

    @avg_trade_rate_description.setter
    def avg_trade_rate_description(self, value: dict):
        self._property_changed('avg_trade_rate_description')
        self.__avg_trade_rate_description = value        

    @property
    def averaging_method_leg1(self) -> dict:
        return self.__averaging_method_leg1

    @averaging_method_leg1.setter
    def averaging_method_leg1(self, value: dict):
        self._property_changed('averaging_method_leg1')
        self.__averaging_method_leg1 = value        

    @property
    def fraction(self) -> dict:
        return self.__fraction

    @fraction.setter
    def fraction(self, value: dict):
        self._property_changed('fraction')
        self.__fraction = value        

    @property
    def sts_credit_market(self) -> dict:
        return self.__sts_credit_market

    @sts_credit_market.setter
    def sts_credit_market(self, value: dict):
        self._property_changed('sts_credit_market')
        self.__sts_credit_market = value        

    @property
    def asset_count_short(self) -> dict:
        return self.__asset_count_short

    @asset_count_short.setter
    def asset_count_short(self, value: dict):
        self._property_changed('asset_count_short')
        self.__asset_count_short = value        

    @property
    def collateral_percentage_required(self) -> dict:
        return self.__collateral_percentage_required

    @collateral_percentage_required.setter
    def collateral_percentage_required(self, value: dict):
        self._property_changed('collateral_percentage_required')
        self.__collateral_percentage_required = value        

    @property
    def opening_auction(self) -> dict:
        return self.__opening_auction

    @opening_auction.setter
    def opening_auction(self, value: dict):
        self._property_changed('opening_auction')
        self.__opening_auction = value        

    @property
    def total_std_return_since_inception(self) -> dict:
        return self.__total_std_return_since_inception

    @total_std_return_since_inception.setter
    def total_std_return_since_inception(self, value: dict):
        self._property_changed('total_std_return_since_inception')
        self.__total_std_return_since_inception = value        

    @property
    def high_unadjusted(self) -> dict:
        return self.__high_unadjusted

    @high_unadjusted.setter
    def high_unadjusted(self, value: dict):
        self._property_changed('high_unadjusted')
        self.__high_unadjusted = value        

    @property
    def source_category(self) -> dict:
        return self.__source_category

    @source_category.setter
    def source_category(self, value: dict):
        self._property_changed('source_category')
        self.__source_category = value        

    @property
    def tv_product_mnemonic(self) -> dict:
        return self.__tv_product_mnemonic

    @tv_product_mnemonic.setter
    def tv_product_mnemonic(self, value: dict):
        self._property_changed('tv_product_mnemonic')
        self.__tv_product_mnemonic = value        

    @property
    def volume_unadjusted(self) -> dict:
        return self.__volume_unadjusted

    @volume_unadjusted.setter
    def volume_unadjusted(self, value: dict):
        self._property_changed('volume_unadjusted')
        self.__volume_unadjusted = value        

    @property
    def price_to_earnings(self) -> dict:
        return self.__price_to_earnings

    @price_to_earnings.setter
    def price_to_earnings(self, value: dict):
        self._property_changed('price_to_earnings')
        self.__price_to_earnings = value        

    @property
    def avg_trade_rate_label(self) -> tuple:
        return self.__avg_trade_rate_label

    @avg_trade_rate_label.setter
    def avg_trade_rate_label(self, value: tuple):
        self._property_changed('avg_trade_rate_label')
        self.__avg_trade_rate_label = value        

    @property
    def ann_yield3_month(self) -> dict:
        return self.__ann_yield3_month

    @ann_yield3_month.setter
    def ann_yield3_month(self, value: dict):
        self._property_changed('ann_yield3_month')
        self.__ann_yield3_month = value        

    @property
    def net_flow_std(self) -> dict:
        return self.__net_flow_std

    @net_flow_std.setter
    def net_flow_std(self, value: dict):
        self._property_changed('net_flow_std')
        self.__net_flow_std = value        

    @property
    def encoded_stats(self) -> dict:
        return self.__encoded_stats

    @encoded_stats.setter
    def encoded_stats(self, value: dict):
        self._property_changed('encoded_stats')
        self.__encoded_stats = value        

    @property
    def ask_size(self) -> dict:
        return self.__ask_size

    @ask_size.setter
    def ask_size(self, value: dict):
        self._property_changed('ask_size')
        self.__ask_size = value        

    @property
    def std30_days_unsubsidized_yield(self) -> dict:
        return self.__std30_days_unsubsidized_yield

    @std30_days_unsubsidized_yield.setter
    def std30_days_unsubsidized_yield(self, value: dict):
        self._property_changed('std30_days_unsubsidized_yield')
        self.__std30_days_unsubsidized_yield = value        

    @property
    def resource(self) -> dict:
        return self.__resource

    @resource.setter
    def resource(self, value: dict):
        self._property_changed('resource')
        self.__resource = value        

    @property
    def price_to_cash(self) -> dict:
        return self.__price_to_cash

    @price_to_cash.setter
    def price_to_cash(self, value: dict):
        self._property_changed('price_to_cash')
        self.__price_to_cash = value        

    @property
    def average_realized_volatility(self) -> dict:
        return self.__average_realized_volatility

    @average_realized_volatility.setter
    def average_realized_volatility(self, value: dict):
        self._property_changed('average_realized_volatility')
        self.__average_realized_volatility = value        

    @property
    def nav_spread(self) -> dict:
        return self.__nav_spread

    @nav_spread.setter
    def nav_spread(self, value: dict):
        self._property_changed('nav_spread')
        self.__nav_spread = value        

    @property
    def bid_price(self) -> dict:
        return self.__bid_price

    @bid_price.setter
    def bid_price(self, value: dict):
        self._property_changed('bid_price')
        self.__bid_price = value        

    @property
    def dollar_total_return(self) -> dict:
        return self.__dollar_total_return

    @dollar_total_return.setter
    def dollar_total_return(self, value: dict):
        self._property_changed('dollar_total_return')
        self.__dollar_total_return = value        

    @property
    def block_unit(self) -> dict:
        return self.__block_unit

    @block_unit.setter
    def block_unit(self, value: dict):
        self._property_changed('block_unit')
        self.__block_unit = value        

    @property
    def es_numeric_percentile(self) -> dict:
        return self.__es_numeric_percentile

    @es_numeric_percentile.setter
    def es_numeric_percentile(self, value: dict):
        self._property_changed('es_numeric_percentile')
        self.__es_numeric_percentile = value        

    @property
    def repurchase_rate(self) -> dict:
        return self.__repurchase_rate

    @repurchase_rate.setter
    def repurchase_rate(self, value: dict):
        self._property_changed('repurchase_rate')
        self.__repurchase_rate = value        

    @property
    def csa_terms(self) -> dict:
        return self.__csa_terms

    @csa_terms.setter
    def csa_terms(self, value: dict):
        self._property_changed('csa_terms')
        self.__csa_terms = value        

    @property
    def daily_net_shareholder_flows(self) -> dict:
        return self.__daily_net_shareholder_flows

    @daily_net_shareholder_flows.setter
    def daily_net_shareholder_flows(self, value: dict):
        self._property_changed('daily_net_shareholder_flows')
        self.__daily_net_shareholder_flows = value        

    @property
    def ask_gspread(self) -> dict:
        return self.__ask_gspread

    @ask_gspread.setter
    def ask_gspread(self, value: dict):
        self._property_changed('ask_gspread')
        self.__ask_gspread = value        

    @property
    def cal_spread_mis_pricing(self) -> dict:
        return self.__cal_spread_mis_pricing

    @cal_spread_mis_pricing.setter
    def cal_spread_mis_pricing(self, value: dict):
        self._property_changed('cal_spread_mis_pricing')
        self.__cal_spread_mis_pricing = value        

    @property
    def leg_two_type(self) -> dict:
        return self.__leg_two_type

    @leg_two_type.setter
    def leg_two_type(self, value: dict):
        self._property_changed('leg_two_type')
        self.__leg_two_type = value        

    @property
    def rate366(self) -> dict:
        return self.__rate366

    @rate366.setter
    def rate366(self, value: dict):
        self._property_changed('rate366')
        self.__rate366 = value        

    @property
    def rate365(self) -> dict:
        return self.__rate365

    @rate365.setter
    def rate365(self, value: dict):
        self._property_changed('rate365')
        self.__rate365 = value        

    @property
    def rate360(self) -> dict:
        return self.__rate360

    @rate360.setter
    def rate360(self, value: dict):
        self._property_changed('rate360')
        self.__rate360 = value        

    @property
    def delivery_point_leg1(self) -> dict:
        return self.__delivery_point_leg1

    @delivery_point_leg1.setter
    def delivery_point_leg1(self, value: dict):
        self._property_changed('delivery_point_leg1')
        self.__delivery_point_leg1 = value        

    @property
    def opening_report(self) -> dict:
        return self.__opening_report

    @opening_report.setter
    def opening_report(self, value: dict):
        self._property_changed('opening_report')
        self.__opening_report = value        

    @property
    def value(self) -> dict:
        return self.__value

    @value.setter
    def value(self, value: dict):
        self._property_changed('value')
        self.__value = value        

    @property
    def leg_one_index_location(self) -> dict:
        return self.__leg_one_index_location

    @leg_one_index_location.setter
    def leg_one_index_location(self, value: dict):
        self._property_changed('leg_one_index_location')
        self.__leg_one_index_location = value        

    @property
    def product_type(self) -> dict:
        return self.__product_type

    @product_type.setter
    def product_type(self, value: dict):
        self._property_changed('product_type')
        self.__product_type = value        

    @property
    def quantity(self) -> dict:
        return self.__quantity

    @quantity.setter
    def quantity(self, value: dict):
        self._property_changed('quantity')
        self.__quantity = value        

    @property
    def report_id(self) -> dict:
        return self.__report_id

    @report_id.setter
    def report_id(self, value: dict):
        self._property_changed('report_id')
        self.__report_id = value        

    @property
    def index_weight(self) -> dict:
        return self.__index_weight

    @index_weight.setter
    def index_weight(self, value: dict):
        self._property_changed('index_weight')
        self.__index_weight = value        

    @property
    def macs_primary_asset_class(self) -> dict:
        return self.__macs_primary_asset_class

    @macs_primary_asset_class.setter
    def macs_primary_asset_class(self, value: dict):
        self._property_changed('macs_primary_asset_class')
        self.__macs_primary_asset_class = value        

    @property
    def midcurve_atm_fwd_rate(self) -> dict:
        return self.__midcurve_atm_fwd_rate

    @midcurve_atm_fwd_rate.setter
    def midcurve_atm_fwd_rate(self, value: dict):
        self._property_changed('midcurve_atm_fwd_rate')
        self.__midcurve_atm_fwd_rate = value        

    @property
    def trader(self) -> dict:
        return self.__trader

    @trader.setter
    def trader(self, value: dict):
        self._property_changed('trader')
        self.__trader = value        

    @property
    def equity_risk_premium_index(self) -> dict:
        return self.__equity_risk_premium_index

    @equity_risk_premium_index.setter
    def equity_risk_premium_index(self, value: dict):
        self._property_changed('equity_risk_premium_index')
        self.__equity_risk_premium_index = value        

    @property
    def clearing_house(self) -> dict:
        return self.__clearing_house

    @clearing_house.setter
    def clearing_house(self, value: dict):
        self._property_changed('clearing_house')
        self.__clearing_house = value        

    @property
    def sts_rates_maturity(self) -> dict:
        return self.__sts_rates_maturity

    @sts_rates_maturity.setter
    def sts_rates_maturity(self, value: dict):
        self._property_changed('sts_rates_maturity')
        self.__sts_rates_maturity = value        

    @property
    def valuation_date(self) -> dict:
        return self.__valuation_date

    @valuation_date.setter
    def valuation_date(self, value: dict):
        self._property_changed('valuation_date')
        self.__valuation_date = value        

    @property
    def restrict_gs_federation(self) -> dict:
        return self.__restrict_gs_federation

    @restrict_gs_federation.setter
    def restrict_gs_federation(self, value: dict):
        self._property_changed('restrict_gs_federation')
        self.__restrict_gs_federation = value        

    @property
    def position_source(self) -> dict:
        return self.__position_source

    @position_source.setter
    def position_source(self, value: dict):
        self._property_changed('position_source')
        self.__position_source = value        

    @property
    def tcm_cost_horizon6_hour(self) -> dict:
        return self.__tcm_cost_horizon6_hour

    @tcm_cost_horizon6_hour.setter
    def tcm_cost_horizon6_hour(self, value: dict):
        self._property_changed('tcm_cost_horizon6_hour')
        self.__tcm_cost_horizon6_hour = value        

    @property
    def liq_dly(self) -> dict:
        return self.__liq_dly

    @liq_dly.setter
    def liq_dly(self, value: dict):
        self._property_changed('liq_dly')
        self.__liq_dly = value        

    @property
    def price_to_book(self) -> dict:
        return self.__price_to_book

    @price_to_book.setter
    def price_to_book(self, value: dict):
        self._property_changed('price_to_book')
        self.__price_to_book = value        

    @property
    def isin(self) -> dict:
        return self.__isin

    @isin.setter
    def isin(self, value: dict):
        self._property_changed('isin')
        self.__isin = value        


class FieldValueMap(Base):
        
    @camel_case_translate
    def __init__(
        self,
        **kwargs
    ):        
        super().__init__()
        self.collateral_value_variance = kwargs.get('collateral_value_variance')
        self.year = kwargs.get('year')
        self.investment_rate = kwargs.get('investment_rate')
        self.forecast_period = kwargs.get('forecast_period')
        self.data_set_ids = kwargs.get('data_set_ids')
        self.bid_unadjusted = kwargs.get('bid_unadjusted')
        self.client_type = kwargs.get('client_type')
        self.available_inventory = kwargs.get('available_inventory')
        self.est1_day_complete_pct = kwargs.get('est1_day_complete_pct')
        self.created_by_id = kwargs.get('created_by_id')
        self.vehicle_type = kwargs.get('vehicle_type')
        self.daily_risk = kwargs.get('daily_risk')
        self.energy = kwargs.get('energy')
        self.market_data_type = kwargs.get('market_data_type')
        self.real_short_rates_contribution = kwargs.get('real_short_rates_contribution')
        self.sentiment_score = kwargs.get('sentiment_score')
        self.leg_one_payment_type = kwargs.get('leg_one_payment_type')
        self.provide_tape_c = kwargs.get('provide_tape_c')
        self.value_previous = kwargs.get('value_previous')
        self.delivery_point_leg2 = kwargs.get('delivery_point_leg2')
        self.avg_trade_rate = kwargs.get('avg_trade_rate')
        self.short_level = kwargs.get('short_level')
        self.version = kwargs.get('version')
        self.policy_rate_expectation = kwargs.get('policy_rate_expectation')
        self.exposure = kwargs.get('exposure')
        self.market_data_asset = kwargs.get('market_data_asset')
        self.earnings_per_share_positive = kwargs.get('earnings_per_share_positive')
        self.unadjusted_high = kwargs.get('unadjusted_high')
        self.source_importance = kwargs.get('source_importance')
        self.relative_return_qtd = kwargs.get('relative_return_qtd')
        self.minutes_to_trade100_pct = kwargs.get('minutes_to_trade100_pct')
        self.expiration_tenor = kwargs.get('expiration_tenor')
        self.market_model_id = kwargs.get('market_model_id')
        self.realized_correlation = kwargs.get('realized_correlation')
        self.collateral_value_actual = kwargs.get('collateral_value_actual')
        self.upfront_payment = kwargs.get('upfront_payment')
        self.atm_fwd_rate = kwargs.get('atm_fwd_rate')
        self.provide_tape_a = kwargs.get('provide_tape_a')
        self.provide_tape_b = kwargs.get('provide_tape_b')
        self.tcm_cost_participation_rate75_pct = kwargs.get('tcm_cost_participation_rate75_pct')
        self.close = kwargs.get('close')
        self.a = kwargs.get('a')
        self.b = kwargs.get('b')
        self.c = kwargs.get('c')
        self.equity_vega = kwargs.get('equity_vega')
        self.leg_one_spread = kwargs.get('leg_one_spread')
        self.lender_payment = kwargs.get('lender_payment')
        self.five_day_move = kwargs.get('five_day_move')
        self.geography_name = kwargs.get('geography_name')
        self.borrower = kwargs.get('borrower')
        self.value_format = kwargs.get('value_format')
        self.performance_contribution = kwargs.get('performance_contribution')
        self.target_notional = kwargs.get('target_notional')
        self.fill_leg_id = kwargs.get('fill_leg_id')
        self.rationale = kwargs.get('rationale')
        self.mkt_class = kwargs.get('mkt_class')
        self.last_updated_since = kwargs.get('last_updated_since')
        self.equities_contribution = kwargs.get('equities_contribution')
        self.congestion = kwargs.get('congestion')
        self.event_category = kwargs.get('event_category')
        self.short_rates_contribution = kwargs.get('short_rates_contribution')
        self.unadjusted_open = kwargs.get('unadjusted_open')
        self.criticality = kwargs.get('criticality')
        self.mtm_price = kwargs.get('mtm_price')
        self.bid_ask_spread = kwargs.get('bid_ask_spread')
        self.leg_one_averaging_method = kwargs.get('leg_one_averaging_method')
        self.option_type = kwargs.get('option_type')
        self.portfolio_assets = kwargs.get('portfolio_assets')
        self.termination_date = kwargs.get('termination_date')
        self.tcm_cost_horizon3_hour = kwargs.get('tcm_cost_horizon3_hour')
        self.number_covered = kwargs.get('number_covered')
        self.credit_limit = kwargs.get('credit_limit')
        self.number_of_positions = kwargs.get('number_of_positions')
        self.effective_tenor = kwargs.get('effective_tenor')
        self.open_unadjusted = kwargs.get('open_unadjusted')
        self.ask_price = kwargs.get('ask_price')
        self.event_id = kwargs.get('event_id')
        self.sectors = kwargs.get('sectors')
        self.std30_days_subsidized_yield = kwargs.get('std30_days_subsidized_yield')
        self.annualized_tracking_error = kwargs.get('annualized_tracking_error')
        self.additional_price_notation_type = kwargs.get('additional_price_notation_type')
        self.vol_swap = kwargs.get('vol_swap')
        self.real_fci = kwargs.get('real_fci')
        self.annualized_risk = kwargs.get('annualized_risk')
        self.block_trades_and_large_notional_off_facility_swaps = kwargs.get(
            'block_trades_and_large_notional_off_facility_swaps')
        self.leg_one_fixed_payment_currency = kwargs.get('leg_one_fixed_payment_currency')
        self.gross_exposure = kwargs.get('gross_exposure')
        self.payment_frequency_leg1 = kwargs.get('payment_frequency_leg1')
        self.payment_frequency_leg2 = kwargs.get('payment_frequency_leg2')
        self.volume_composite = kwargs.get('volume_composite')
        self.volume = kwargs.get('volume')
        self.adv = kwargs.get('adv')
        self.external = kwargs.get('external')
        self.short_conviction_medium = kwargs.get('short_conviction_medium')
        self.exchange = kwargs.get('exchange')
        self.trade_price = kwargs.get('trade_price')
        self.cleared = kwargs.get('cleared')
        self.es_policy_score = kwargs.get('es_policy_score')
        self.prime_id_numeric = kwargs.get('prime_id_numeric')
        self.leg_one_index = kwargs.get('leg_one_index')
        self.on_loan_percentage = kwargs.get('on_loan_percentage')
        self.bid_high = kwargs.get('bid_high')
        self.fair_variance = kwargs.get('fair_variance')
        self.hit_rate_wtd = kwargs.get('hit_rate_wtd')
        self.bos_in_bps_description = kwargs.get('bos_in_bps_description')
        self.low_price = kwargs.get('low_price')
        self.realized_volatility = kwargs.get('realized_volatility')
        self.adv22_day_pct = kwargs.get('adv22_day_pct')
        self.clone_parent_id = kwargs.get('clone_parent_id')
        self.price_range_in_ticks_label = kwargs.get('price_range_in_ticks_label')
        self.ticker = kwargs.get('ticker')
        self.tcm_cost_horizon1_day = kwargs.get('tcm_cost_horizon1_day')
        self.approval = kwargs.get('approval')
        self.file_location = kwargs.get('file_location')
        self.leg_two_payment_type = kwargs.get('leg_two_payment_type')
        self.horizon = kwargs.get('horizon')
        self.day_count_convention_leg1 = kwargs.get('day_count_convention_leg1')
        self.source_value_forecast = kwargs.get('source_value_forecast')
        self.short_conviction_large = kwargs.get('short_conviction_large')
        self.day_count_convention_leg2 = kwargs.get('day_count_convention_leg2')
        self.counter_party_status = kwargs.get('counter_party_status')
        self.composite22_day_adv = kwargs.get('composite22_day_adv')
        self.dollar_excess_return = kwargs.get('dollar_excess_return')
        self.trade_end_date = kwargs.get('trade_end_date')
        self.percent_of_mediandv1m = kwargs.get('percent_of_mediandv1m')
        self.lendables = kwargs.get('lendables')
        self.loan_spread_required = kwargs.get('loan_spread_required')
        self.asset_class = kwargs.get('asset_class')
        self.sovereign_spread_contribution = kwargs.get('sovereign_spread_contribution')
        self.bos_in_ticks_label = kwargs.get('bos_in_ticks_label')
        self.ric = kwargs.get('ric')
        self.position_source_id = kwargs.get('position_source_id')
        self.rate_type = kwargs.get('rate_type')
        self.gs_sustain_region = kwargs.get('gs_sustain_region')
        self.deployment_id = kwargs.get('deployment_id')
        self.loan_status = kwargs.get('loan_status')
        self.short_weight = kwargs.get('short_weight')
        self.geography_id = kwargs.get('geography_id')
        self.loan_rebate = kwargs.get('loan_rebate')
        self.period = kwargs.get('period')
        self.index_create_source = kwargs.get('index_create_source')
        self.fiscal_quarter = kwargs.get('fiscal_quarter')
        self.version_string = kwargs.get('version_string')
        self.real_twi_contribution = kwargs.get('real_twi_contribution')
        self.market_impact = kwargs.get('market_impact')
        self.event_type = kwargs.get('event_type')
        self.mkt_asset = kwargs.get('mkt_asset')
        self.asset_count_long = kwargs.get('asset_count_long')
        self.spot = kwargs.get('spot')
        self.last_updated_message = kwargs.get('last_updated_message')
        self.underlying_asset_leg2 = kwargs.get('underlying_asset_leg2')
        self.loan_value = kwargs.get('loan_value')
        self.underlying_asset_leg1 = kwargs.get('underlying_asset_leg1')
        self.swap_spread = kwargs.get('swap_spread')
        self.trading_restriction = kwargs.get('trading_restriction')
        self.asset_parameters_pay_or_receive = kwargs.get('asset_parameters_pay_or_receive')
        self.price_spot_entry_unit = kwargs.get('price_spot_entry_unit')
        self.total_return_price = kwargs.get('total_return_price')
        self.weighted_percent_in_model = kwargs.get('weighted_percent_in_model')
        self.election_period = kwargs.get('election_period')
        self.funding_ask_price = kwargs.get('funding_ask_price')
        self.historical_beta = kwargs.get('historical_beta')
        self.dissemination_id = kwargs.get('dissemination_id')
        self.bond_risk_premium_index = kwargs.get('bond_risk_premium_index')
        self.leg_two_fixed_payment = kwargs.get('leg_two_fixed_payment')
        self.commodity_forecast = kwargs.get('commodity_forecast')
        self.hit_rate_ytd = kwargs.get('hit_rate_ytd')
        self.valid = kwargs.get('valid')
        self.initial_pricing_date = kwargs.get('initial_pricing_date')
        self.indication_of_end_user_exception = kwargs.get('indication_of_end_user_exception')
        self.es_score = kwargs.get('es_score')
        self.price_range_in_ticks = kwargs.get('price_range_in_ticks')
        self.expense_ratio_gross_bps = kwargs.get('expense_ratio_gross_bps')
        self.pct_change = kwargs.get('pct_change')
        self.number_of_rolls = kwargs.get('number_of_rolls')
        self.agent_lender_fee = kwargs.get('agent_lender_fee')
        self.bbid = kwargs.get('bbid')
        self.option_strike_price = kwargs.get('option_strike_price')
        self.effective_date = kwargs.get('effective_date')
        self.price_type_leg3 = kwargs.get('price_type_leg3')
        self.arrival_mid_normalized = kwargs.get('arrival_mid_normalized')
        self.underlying_asset2 = kwargs.get('underlying_asset2')
        self.underlying_asset1 = kwargs.get('underlying_asset1')
        self.rounded_notional_amount_leg1 = kwargs.get('rounded_notional_amount_leg1')
        self.rounded_notional_amount_leg2 = kwargs.get('rounded_notional_amount_leg2')
        self.capped = kwargs.get('capped')
        self.rating = kwargs.get('rating')
        self.payment_type_leg1 = kwargs.get('payment_type_leg1')
        self.option_currency = kwargs.get('option_currency')
        self.price_leg3 = kwargs.get('price_leg3')
        self.price_leg2 = kwargs.get('price_leg2')
        self.price_leg1 = kwargs.get('price_leg1')
        self.price_type_leg2 = kwargs.get('price_type_leg2')
        self.legal_entity = kwargs.get('legal_entity')
        self.performance_fee = kwargs.get('performance_fee')
        self.price_type_leg1 = kwargs.get('price_type_leg1')
        self.payment_type_leg2 = kwargs.get('payment_type_leg2')
        self.type_leg1 = kwargs.get('type_leg1')
        self.underlying_asset_ids = kwargs.get('underlying_asset_ids')
        self.type_leg2 = kwargs.get('type_leg2')
        self.queue_in_lots_label = kwargs.get('queue_in_lots_label')
        self.adv10_day_pct = kwargs.get('adv10_day_pct')
        self.long_conviction_medium = kwargs.get('long_conviction_medium')
        self.annual_risk = kwargs.get('annual_risk')
        self.eti = kwargs.get('eti')
        self.daily_tracking_error = kwargs.get('daily_tracking_error')
        self.leg_two_index = kwargs.get('leg_two_index')
        self.market_buffer = kwargs.get('market_buffer')
        self.market_cap = kwargs.get('market_cap')
        self.oe_id = kwargs.get('oe_id')
        self.cluster_region = kwargs.get('cluster_region')
        self.bbid_equivalent = kwargs.get('bbid_equivalent')
        self.valoren = kwargs.get('valoren')
        self.basis = kwargs.get('basis')
        self.investment_rate_trend = kwargs.get('investment_rate_trend')
        self.ext_mkt_class = kwargs.get('ext_mkt_class')
        self.price_currency = kwargs.get('price_currency')
        self.hedge_id = kwargs.get('hedge_id')
        self.tcm_cost_horizon8_day = kwargs.get('tcm_cost_horizon8_day')
        self.residual_variance = kwargs.get('residual_variance')
        self.supra_strategy = kwargs.get('supra_strategy')
        self.restrict_internal_derived_data = kwargs.get('restrict_internal_derived_data')
        self.day_count_convention = kwargs.get('day_count_convention')
        self.rounded_notional_amount1 = kwargs.get('rounded_notional_amount1')
        self.adv5_day_pct = kwargs.get('adv5_day_pct')
        self.rounded_notional_amount2 = kwargs.get('rounded_notional_amount2')
        self.lending_sec_type = kwargs.get('lending_sec_type')
        self.leverage = kwargs.get('leverage')
        self.option_family = kwargs.get('option_family')
        self.price_spot_stop_loss_value = kwargs.get('price_spot_stop_loss_value')
        self.kpi_id = kwargs.get('kpi_id')
        self.relative_return_wtd = kwargs.get('relative_return_wtd')
        self.borrow_cost = kwargs.get('borrow_cost')
        self.average_implied_volatility = kwargs.get('average_implied_volatility')
        self.fair_value = kwargs.get('fair_value')
        self.adjusted_high_price = kwargs.get('adjusted_high_price')
        self.open_time = kwargs.get('open_time')
        self.local_ccy_rate = kwargs.get('local_ccy_rate')
        self.ext_mkt_point1 = kwargs.get('ext_mkt_point1')
        self.direction = kwargs.get('direction')
        self.ext_mkt_point2 = kwargs.get('ext_mkt_point2')
        self.sub_region_code = kwargs.get('sub_region_code')
        self.value_forecast = kwargs.get('value_forecast')
        self.execution_venue = kwargs.get('execution_venue')
        self.position_source_type = kwargs.get('position_source_type')
        self.approve_rebalance = kwargs.get('approve_rebalance')
        self.adjusted_close_price = kwargs.get('adjusted_close_price')
        self.lms_id = kwargs.get('lms_id')
        self.rebate_rate = kwargs.get('rebate_rate')
        self.participation_rate = kwargs.get('participation_rate')
        self.obfr = kwargs.get('obfr')
        self.option_lock_period = kwargs.get('option_lock_period')
        self.strike_relative = kwargs.get('strike_relative')
        self.es_momentum_percentile = kwargs.get('es_momentum_percentile')
        self.price_notation = kwargs.get('price_notation')
        self.strategy = kwargs.get('strategy')
        self.forecast_date = kwargs.get('forecast_date')
        self.position_type = kwargs.get('position_type')
        self.lender_income = kwargs.get('lender_income')
        self.sub_asset_class = kwargs.get('sub_asset_class')
        self.provide_mpl_tape_b = kwargs.get('provide_mpl_tape_b')
        self.short_interest = kwargs.get('short_interest')
        self.reference_period = kwargs.get('reference_period')
        self.provide_mpl_tape_c = kwargs.get('provide_mpl_tape_c')
        self.adjusted_volume = kwargs.get('adjusted_volume')
        self.provide_mpl_tape_a = kwargs.get('provide_mpl_tape_a')
        self.owner_id = kwargs.get('owner_id')
        self.composite10_day_adv = kwargs.get('composite10_day_adv')
        self.bpe_quality_stars = kwargs.get('bpe_quality_stars')
        self.idea_activity_type = kwargs.get('idea_activity_type')
        self.idea_source = kwargs.get('idea_source')
        self.unadjusted_ask = kwargs.get('unadjusted_ask')
        self.trading_pnl = kwargs.get('trading_pnl')
        self.collateral_value_required = kwargs.get('collateral_value_required')
        self.given_plus_paid = kwargs.get('given_plus_paid')
        self.short_conviction_small = kwargs.get('short_conviction_small')
        self.price_to_earnings_positive = kwargs.get('price_to_earnings_positive')
        self.forecast = kwargs.get('forecast')
        self.pnl = kwargs.get('pnl')
        self.upfront_payment_currency = kwargs.get('upfront_payment_currency')
        self.date_index = kwargs.get('date_index')
        self.tcm_cost_horizon4_day = kwargs.get('tcm_cost_horizon4_day')
        self.asset_classifications_is_primary = kwargs.get('asset_classifications_is_primary')
        self.styles = kwargs.get('styles')
        self.short_name = kwargs.get('short_name')
        self.dwi_contribution = kwargs.get('dwi_contribution')
        self.reset_frequency1 = kwargs.get('reset_frequency1')
        self.asset2_id = kwargs.get('asset2_id')
        self.reset_frequency2 = kwargs.get('reset_frequency2')
        self.average_fill_price = kwargs.get('average_fill_price')
        self.price_notation_type2 = kwargs.get('price_notation_type2')
        self.price_notation_type3 = kwargs.get('price_notation_type3')
        self.bid_gspread = kwargs.get('bid_gspread')
        self.open_price = kwargs.get('open_price')
        self.depth_spread_score = kwargs.get('depth_spread_score')
        self.sub_account = kwargs.get('sub_account')
        self.notional_currency_leg1 = kwargs.get('notional_currency_leg1')
        self.notional_currency_leg2 = kwargs.get('notional_currency_leg2')
        self.fair_volatility = kwargs.get('fair_volatility')
        self.portfolio_type = kwargs.get('portfolio_type')
        self.vendor = kwargs.get('vendor')
        self.currency = kwargs.get('currency')
        self.cluster_class = kwargs.get('cluster_class')
        self.queueing_time = kwargs.get('queueing_time')
        self.ann_return5_year = kwargs.get('ann_return5_year')
        self.bid_size = kwargs.get('bid_size')
        self.arrival_mid = kwargs.get('arrival_mid')
        self.business_sponsor = kwargs.get('business_sponsor')
        self.asset_parameters_exchange_currency = kwargs.get('asset_parameters_exchange_currency')
        self.unexplained = kwargs.get('unexplained')
        self.candidate_name = kwargs.get('candidate_name')
        self.metric = kwargs.get('metric')
        self.ask = kwargs.get('ask')
        self.close_price = kwargs.get('close_price')
        self.end_time = kwargs.get('end_time')
        self.execution_timestamp = kwargs.get('execution_timestamp')
        self.source = kwargs.get('source')
        self.expense_ratio_net_bps = kwargs.get('expense_ratio_net_bps')
        self.data_set_sub_category = kwargs.get('data_set_sub_category')
        self.day_count_convention2 = kwargs.get('day_count_convention2')
        self.quantity_bucket = kwargs.get('quantity_bucket')
        self.factor_two = kwargs.get('factor_two')
        self.oe_name = kwargs.get('oe_name')
        self.given = kwargs.get('given')
        self.delisting_date = kwargs.get('delisting_date')
        self.price_spot_target_value = kwargs.get('price_spot_target_value')
        self.weight = kwargs.get('weight')
        self.business_scope = kwargs.get('business_scope')
        self.market_data_point = kwargs.get('market_data_point')
        self.absolute_weight = kwargs.get('absolute_weight')
        self.trade_time = kwargs.get('trade_time')
        self.measure = kwargs.get('measure')
        self.hedge_annualized_volatility = kwargs.get('hedge_annualized_volatility')
        self.benchmark_currency = kwargs.get('benchmark_currency')
        self.futures_contract = kwargs.get('futures_contract')
        self.name = kwargs.get('name')
        self.aum = kwargs.get('aum')
        self.folder_name = kwargs.get('folder_name')
        self.option_expiration_date = kwargs.get('option_expiration_date')
        self.swaption_atm_fwd_rate = kwargs.get('swaption_atm_fwd_rate')
        self.live_date = kwargs.get('live_date')
        self.ask_high = kwargs.get('ask_high')
        self.corporate_action_type = kwargs.get('corporate_action_type')
        self.prime_id = kwargs.get('prime_id')
        self.region_name = kwargs.get('region_name')
        self.description = kwargs.get('description')
        self.asset_classifications_is_country_primary = kwargs.get('asset_classifications_is_country_primary')
        self.value_revised = kwargs.get('value_revised')
        self.adjusted_trade_price = kwargs.get('adjusted_trade_price')
        self.forecast_time = kwargs.get('forecast_time')
        self.is_adr = kwargs.get('is_adr')
        self.factor = kwargs.get('factor')
        self.days_on_loan = kwargs.get('days_on_loan')
        self.long_conviction_small = kwargs.get('long_conviction_small')
        self.service_id = kwargs.get('service_id')
        self.gsfeer = kwargs.get('gsfeer')
        self.wam = kwargs.get('wam')
        self.wal = kwargs.get('wal')
        self.backtest_id = kwargs.get('backtest_id')
        self.leg_two_index_location = kwargs.get('leg_two_index_location')
        self.g_score = kwargs.get('g_score')
        self.corporate_spread_contribution = kwargs.get('corporate_spread_contribution')
        self.market_value = kwargs.get('market_value')
        self.notional_currency1 = kwargs.get('notional_currency1')
        self.net_debt_to_ebitda = kwargs.get('net_debt_to_ebitda')
        self.notional_currency2 = kwargs.get('notional_currency2')
        self.multiple_score = kwargs.get('multiple_score')
        self.beta_adjusted_exposure = kwargs.get('beta_adjusted_exposure')
        self.paid = kwargs.get('paid')
        self.short = kwargs.get('short')
        self.bos_in_ticks_description = kwargs.get('bos_in_ticks_description')
        self.time = kwargs.get('time')
        self.implied_correlation = kwargs.get('implied_correlation')
        self.event_end_date_time = kwargs.get('event_end_date_time')
        self.normalized_performance = kwargs.get('normalized_performance')
        self.taxonomy = kwargs.get('taxonomy')
        self.swaption_vol = kwargs.get('swaption_vol')
        self.source_origin = kwargs.get('source_origin')
        self.measures = kwargs.get('measures')
        self.total_quantity = kwargs.get('total_quantity')
        self.internal_user = kwargs.get('internal_user')
        self.created_time = kwargs.get('created_time')
        self.identifier = kwargs.get('identifier')
        self.price_unit = kwargs.get('price_unit')
        self.redemption_option = kwargs.get('redemption_option')
        self.notional_unit2 = kwargs.get('notional_unit2')
        self.unadjusted_low = kwargs.get('unadjusted_low')
        self.notional_unit1 = kwargs.get('notional_unit1')
        self.sedol = kwargs.get('sedol')
        self.rounding_cost_pnl = kwargs.get('rounding_cost_pnl')
        self.sustain_global = kwargs.get('sustain_global')
        self.portfolio_id = kwargs.get('portfolio_id')
        self.ending_date = kwargs.get('ending_date')
        self.cap_floor_atm_fwd_rate = kwargs.get('cap_floor_atm_fwd_rate')
        self.es_percentile = kwargs.get('es_percentile')
        self.ann_return3_year = kwargs.get('ann_return3_year')
        self.rcic = kwargs.get('rcic')
        self.hit_rate_qtd = kwargs.get('hit_rate_qtd')
        self.fci = kwargs.get('fci')
        self.recall_quantity = kwargs.get('recall_quantity')
        self.premium = kwargs.get('premium')
        self.low = kwargs.get('low')
        self.cross_group = kwargs.get('cross_group')
        self.report_run_time = kwargs.get('report_run_time')
        self.five_day_price_change_bps = kwargs.get('five_day_price_change_bps')
        self.holdings = kwargs.get('holdings')
        self.price_method = kwargs.get('price_method')
        self.mid_price = kwargs.get('mid_price')
        self.tcm_cost_horizon2_day = kwargs.get('tcm_cost_horizon2_day')
        self.pending_loan_count = kwargs.get('pending_loan_count')
        self.price_spot_stop_loss_unit = kwargs.get('price_spot_stop_loss_unit')
        self.queue_in_lots = kwargs.get('queue_in_lots')
        self.price_range_in_ticks_description = kwargs.get('price_range_in_ticks_description')
        self.tender_offer_expiration_date = kwargs.get('tender_offer_expiration_date')
        self.primary_country_ric = kwargs.get('primary_country_ric')
        self.leg_one_fixed_payment = kwargs.get('leg_one_fixed_payment')
        self.option_expiration_frequency = kwargs.get('option_expiration_frequency')
        self.lending_fund_nav_trend = kwargs.get('lending_fund_nav_trend')
        self.tcm_cost_participation_rate5_pct = kwargs.get('tcm_cost_participation_rate5_pct')
        self.is_active = kwargs.get('is_active')
        self.growth_score = kwargs.get('growth_score')
        self.buffer_threshold = kwargs.get('buffer_threshold')
        self.price_forming_continuation_data = kwargs.get('price_forming_continuation_data')
        self.adjusted_short_interest = kwargs.get('adjusted_short_interest')
        self.asset_parameters_strike = kwargs.get('asset_parameters_strike')
        self.asset_parameters_termination_date = kwargs.get('asset_parameters_termination_date')
        self.estimated_spread = kwargs.get('estimated_spread')
        self.asset_parameters_effective_date = kwargs.get('asset_parameters_effective_date')
        self.ann_return10_year = kwargs.get('ann_return10_year')
        self.created = kwargs.get('created')
        self.tcm_cost = kwargs.get('tcm_cost')
        self.sustain_japan = kwargs.get('sustain_japan')
        self.fixed_payment_currency_leg1 = kwargs.get('fixed_payment_currency_leg1')
        self.hedge_tracking_error = kwargs.get('hedge_tracking_error')
        self.fixed_payment_currency_leg2 = kwargs.get('fixed_payment_currency_leg2')
        self.market_cap_category = kwargs.get('market_cap_category')
        self.historical_volume = kwargs.get('historical_volume')
        self.strike_price = kwargs.get('strike_price')
        self.event_start_date = kwargs.get('event_start_date')
        self.reset_frequency_leg1 = kwargs.get('reset_frequency_leg1')
        self.reset_frequency_leg2 = kwargs.get('reset_frequency_leg2')
        self.equity_gamma = kwargs.get('equity_gamma')
        self.gross_income = kwargs.get('gross_income')
        self.adjusted_open_price = kwargs.get('adjusted_open_price')
        self.asset_count_in_model = kwargs.get('asset_count_in_model')
        self.country_id = kwargs.get('country_id')
        self.total_returns = kwargs.get('total_returns')
        self.lender = kwargs.get('lender')
        self.ann_return1_year = kwargs.get('ann_return1_year')
        self.min_temperature = kwargs.get('min_temperature')
        self.eff_yield7_day = kwargs.get('eff_yield7_day')
        self.meeting_date = kwargs.get('meeting_date')
        self.close_time = kwargs.get('close_time')
        self.amount = kwargs.get('amount')
        self.lending_fund_acct = kwargs.get('lending_fund_acct')
        self.rebate = kwargs.get('rebate')
        self.flagship = kwargs.get('flagship')
        self.additional_price_notation = kwargs.get('additional_price_notation')
        self.election_type = kwargs.get('election_type')
        self.implied_volatility = kwargs.get('implied_volatility')
        self.spread = kwargs.get('spread')
        self.equity_delta = kwargs.get('equity_delta')
        self.gross_weight = kwargs.get('gross_weight')
        self.listed = kwargs.get('listed')
        self.earnings_record_type = kwargs.get('earnings_record_type')
        self.g10_currency = kwargs.get('g10_currency')
        self.shock_style = kwargs.get('shock_style')
        self.relative_period = kwargs.get('relative_period')
        self.methodology = kwargs.get('methodology')
        self.queue_clock_time_label = kwargs.get('queue_clock_time_label')
        self.market_pnl = kwargs.get('market_pnl')
        self.sustain_asia_ex_japan = kwargs.get('sustain_asia_ex_japan')
        self.index_leg2 = kwargs.get('index_leg2')
        self.index_leg1 = kwargs.get('index_leg1')
        self.swap_rate = kwargs.get('swap_rate')
        self.mixed_swap_other_reported_sdr = kwargs.get('mixed_swap_other_reported_sdr')
        self.data_set_category = kwargs.get('data_set_category')
        self.bos_in_bps_label = kwargs.get('bos_in_bps_label')
        self.bos_in_bps = kwargs.get('bos_in_bps')
        self.fx_spot = kwargs.get('fx_spot')
        self.bid_low = kwargs.get('bid_low')
        self.restrict_named_individuals = kwargs.get('restrict_named_individuals')
        self.fair_variance_volatility = kwargs.get('fair_variance_volatility')
        self.hedge_volatility = kwargs.get('hedge_volatility')
        self.tags = kwargs.get('tags')
        self.real_long_rates_contribution = kwargs.get('real_long_rates_contribution')
        self.client_exposure = kwargs.get('client_exposure')
        self.gs_sustain_sub_sector = kwargs.get('gs_sustain_sub_sector')
        self.domain = kwargs.get('domain')
        self.share_class_assets = kwargs.get('share_class_assets')
        self.annuity = kwargs.get('annuity')
        self.uid = kwargs.get('uid')
        self.es_policy_percentile = kwargs.get('es_policy_percentile')
        self.floating_rate_option = kwargs.get('floating_rate_option')
        self.term = kwargs.get('term')
        self.restrict_internal_gs_ntk = kwargs.get('restrict_internal_gs_ntk')
        self.asset_parameters_clearing_house = kwargs.get('asset_parameters_clearing_house')
        self.tcm_cost_participation_rate100_pct = kwargs.get('tcm_cost_participation_rate100_pct')
        self.disclaimer = kwargs.get('disclaimer')
        self.measure_idx = kwargs.get('measure_idx')
        self.loan_fee = kwargs.get('loan_fee')
        self.deployment_version = kwargs.get('deployment_version')
        self.twi_contribution = kwargs.get('twi_contribution')
        self.delisted = kwargs.get('delisted')
        self.regional_focus = kwargs.get('regional_focus')
        self.volume_primary = kwargs.get('volume_primary')
        self.leg_two_delivery_point = kwargs.get('leg_two_delivery_point')
        self.funding_bid_price = kwargs.get('funding_bid_price')
        self.price_to_sales = kwargs.get('price_to_sales')
        self.closing_auction = kwargs.get('closing_auction')
        self.new_ideas_qtd = kwargs.get('new_ideas_qtd')
        self.adjusted_ask_price = kwargs.get('adjusted_ask_price')
        self.quarter = kwargs.get('quarter')
        self.factor_universe = kwargs.get('factor_universe')
        self.asset_parameters_floating_rate_option = kwargs.get('asset_parameters_floating_rate_option')
        self.arrival_rt = kwargs.get('arrival_rt')
        self.vote_share = kwargs.get('vote_share')
        self.excess_margin_value = kwargs.get('excess_margin_value')
        self.transaction_cost = kwargs.get('transaction_cost')
        self.central_bank_swap_rate = kwargs.get('central_bank_swap_rate')
        self.servicing_cost_short_pnl = kwargs.get('servicing_cost_short_pnl')
        self.notional_unit_leg1 = kwargs.get('notional_unit_leg1')
        self.cluster_description = kwargs.get('cluster_description')
        self.notional_unit_leg2 = kwargs.get('notional_unit_leg2')
        self.position_amount = kwargs.get('position_amount')
        self.wind_speed = kwargs.get('wind_speed')
        self.event_start_date_time = kwargs.get('event_start_date_time')
        self.borrower_id = kwargs.get('borrower_id')
        self.data_product = kwargs.get('data_product')
        self.implied_volatility_by_delta_strike = kwargs.get('implied_volatility_by_delta_strike')
        self.bm_prime_id = kwargs.get('bm_prime_id')
        self.corporate_action = kwargs.get('corporate_action')
        self.conviction = kwargs.get('conviction')
        self.gross_flow_normalized = kwargs.get('gross_flow_normalized')
        self.g_regional_score = kwargs.get('g_regional_score')
        self.factor_id = kwargs.get('factor_id')
        self.hard_to_borrow = kwargs.get('hard_to_borrow')
        self.wpk = kwargs.get('wpk')
        self.bid_change = kwargs.get('bid_change')
        self.month = kwargs.get('month')
        self.asset_parameters_expiration_date = kwargs.get('asset_parameters_expiration_date')
        self.expiration = kwargs.get('expiration')
        self.country_name = kwargs.get('country_name')
        self.starting_date = kwargs.get('starting_date')
        self.onboarded = kwargs.get('onboarded')
        self.liquidity_score = kwargs.get('liquidity_score')
        self.spread_leg2 = kwargs.get('spread_leg2')
        self.spread_leg1 = kwargs.get('spread_leg1')
        self.long_rates_contribution = kwargs.get('long_rates_contribution')
        self.importance = kwargs.get('importance')
        self.source_date_span = kwargs.get('source_date_span')
        self.ann_yield6_month = kwargs.get('ann_yield6_month')
        self.underlying_data_set_id = kwargs.get('underlying_data_set_id')
        self.close_unadjusted = kwargs.get('close_unadjusted')
        self.value_unit = kwargs.get('value_unit')
        self.quantity_unit = kwargs.get('quantity_unit')
        self.adjusted_low_price = kwargs.get('adjusted_low_price')
        self.net_exposure_classification = kwargs.get('net_exposure_classification')
        self.settlement_method = kwargs.get('settlement_method')
        self.long_conviction_large = kwargs.get('long_conviction_large')
        self.alpha = kwargs.get('alpha')
        self.company = kwargs.get('company')
        self.conviction_list = kwargs.get('conviction_list')
        self.settlement_frequency = kwargs.get('settlement_frequency')
        self.dist_avg7_day = kwargs.get('dist_avg7_day')
        self.remove_tape_c = kwargs.get('remove_tape_c')
        self.remove_tape_b = kwargs.get('remove_tape_b')
        self.in_risk_model = kwargs.get('in_risk_model')
        self.daily_net_shareholder_flows_percent = kwargs.get('daily_net_shareholder_flows_percent')
        self.type_of_return = kwargs.get('type_of_return')
        self.servicing_cost_long_pnl = kwargs.get('servicing_cost_long_pnl')
        self.excess_margin_percentage = kwargs.get('excess_margin_percentage')
        self.remove_tape_a = kwargs.get('remove_tape_a')
        self.meeting_number = kwargs.get('meeting_number')
        self.exchange_id = kwargs.get('exchange_id')
        self.mid_gspread = kwargs.get('mid_gspread')
        self.tcm_cost_horizon20_day = kwargs.get('tcm_cost_horizon20_day')
        self.long_level = kwargs.get('long_level')
        self.realm = kwargs.get('realm')
        self.bid = kwargs.get('bid')
        self.is_aggressive = kwargs.get('is_aggressive')
        self.order_id = kwargs.get('order_id')
        self.repo_rate = kwargs.get('repo_rate')
        self.market_cap_usd = kwargs.get('market_cap_usd')
        self.high_price = kwargs.get('high_price')
        self.absolute_shares = kwargs.get('absolute_shares')
        self.action = kwargs.get('action')
        self.model = kwargs.get('model')
        self.__id = kwargs.get('id_')
        self.arrival_haircut_vwap_normalized = kwargs.get('arrival_haircut_vwap_normalized')
        self.price_component = kwargs.get('price_component')
        self.queue_clock_time_description = kwargs.get('queue_clock_time_description')
        self.delta_strike = kwargs.get('delta_strike')
        self.asset_parameters_notional_currency = kwargs.get('asset_parameters_notional_currency')
        self.value_actual = kwargs.get('value_actual')
        self.upi = kwargs.get('upi')
        self.asset_types = kwargs.get('asset_types')
        self.bcid = kwargs.get('bcid')
        self.mkt_point = kwargs.get('mkt_point')
        self.collateral_currency = kwargs.get('collateral_currency')
        self.restriction_start_date = kwargs.get('restriction_start_date')
        self.original_country = kwargs.get('original_country')
        self.touch_liquidity_score = kwargs.get('touch_liquidity_score')
        self.field = kwargs.get('field')
        self.factor_category_id = kwargs.get('factor_category_id')
        self.expected_completion_date = kwargs.get('expected_completion_date')
        self.spread_option_vol = kwargs.get('spread_option_vol')
        self.inflation_swap_rate = kwargs.get('inflation_swap_rate')
        self.fx_risk_premium_index = kwargs.get('fx_risk_premium_index')
        self.skew = kwargs.get('skew')
        self.status = kwargs.get('status')
        self.sustain_emerging_markets = kwargs.get('sustain_emerging_markets')
        self.event_date_time = kwargs.get('event_date_time')
        self.total_price = kwargs.get('total_price')
        self.embeded_option = kwargs.get('embeded_option')
        self.event_source = kwargs.get('event_source')
        self.on_behalf_of = kwargs.get('on_behalf_of')
        self.qis_perm_no = kwargs.get('qis_perm_no')
        self.shareclass_id = kwargs.get('shareclass_id')
        self.exception_status = kwargs.get('exception_status')
        self.short_exposure = kwargs.get('short_exposure')
        self.tcm_cost_participation_rate10_pct = kwargs.get('tcm_cost_participation_rate10_pct')
        self.event_time = kwargs.get('event_time')
        self.delivery_date = kwargs.get('delivery_date')
        self.arrival_haircut_vwap = kwargs.get('arrival_haircut_vwap')
        self.interest_rate = kwargs.get('interest_rate')
        self.execution_days = kwargs.get('execution_days')
        self.recall_due_date = kwargs.get('recall_due_date')
        self.side = kwargs.get('side')
        self.forward = kwargs.get('forward')
        self.borrow_fee = kwargs.get('borrow_fee')
        self.update_time = kwargs.get('update_time')
        self.loan_spread = kwargs.get('loan_spread')
        self.tcm_cost_horizon12_hour = kwargs.get('tcm_cost_horizon12_hour')
        self.dew_point = kwargs.get('dew_point')
        self.research_commission = kwargs.get('research_commission')
        self.leg_one_delivery_point = kwargs.get('leg_one_delivery_point')
        self.event_status = kwargs.get('event_status')
        self.sell_date = kwargs.get('sell_date')
        self.asset_parameters_settlement = kwargs.get('asset_parameters_settlement')
        self.__return = kwargs.get('return_')
        self.max_temperature = kwargs.get('max_temperature')
        self.acquirer_shareholder_meeting_date = kwargs.get('acquirer_shareholder_meeting_date')
        self.notional_amount = kwargs.get('notional_amount')
        self.pay_or_receive = kwargs.get('pay_or_receive')
        self.arrival_rt_normalized = kwargs.get('arrival_rt_normalized')
        self.report_type = kwargs.get('report_type')
        self.source_url = kwargs.get('source_url')
        self.estimated_return = kwargs.get('estimated_return')
        self.high = kwargs.get('high')
        self.source_last_update = kwargs.get('source_last_update')
        self.quantity_mw = kwargs.get('quantity_mw')
        self.pnode_id = kwargs.get('pnode_id')
        self.event_name = kwargs.get('event_name')
        self.indication_of_other_price_affecting_term = kwargs.get('indication_of_other_price_affecting_term')
        self.unadjusted_bid = kwargs.get('unadjusted_bid')
        self.backtest_type = kwargs.get('backtest_type')
        self.gsdeer = kwargs.get('gsdeer')
        self.g_regional_percentile = kwargs.get('g_regional_percentile')
        self.prev_close_ask = kwargs.get('prev_close_ask')
        self.level = kwargs.get('level')
        self.mnav = kwargs.get('mnav')
        self.es_momentum_score = kwargs.get('es_momentum_score')
        self.curr_yield7_day = kwargs.get('curr_yield7_day')
        self.pressure = kwargs.get('pressure')
        self.short_description = kwargs.get('short_description')
        self.feed = kwargs.get('feed')
        self.net_weight = kwargs.get('net_weight')
        self.portfolio_managers = kwargs.get('portfolio_managers')
        self.asset_parameters_commodity_sector = kwargs.get('asset_parameters_commodity_sector')
        self.bos_in_ticks = kwargs.get('bos_in_ticks')
        self.price_notation2 = kwargs.get('price_notation2')
        self.market_buffer_threshold = kwargs.get('market_buffer_threshold')
        self.price_notation3 = kwargs.get('price_notation3')
        self.cap_floor_vol = kwargs.get('cap_floor_vol')
        self.notional = kwargs.get('notional')
        self.es_disclosure_percentage = kwargs.get('es_disclosure_percentage')
        self.investment_income = kwargs.get('investment_income')
        self.client_short_name = kwargs.get('client_short_name')
        self.bid_plus_ask = kwargs.get('bid_plus_ask')
        self.foreign_ccy_rate = kwargs.get('foreign_ccy_rate')
        self.election_odds = kwargs.get('election_odds')
        self.require_anon_client_name = kwargs.get('require_anon_client_name')
        self.total = kwargs.get('total')
        self.asset_id = kwargs.get('asset_id')
        self.mkt_type = kwargs.get('mkt_type')
        self.last_updated_time = kwargs.get('last_updated_time')
        self.pricing_location = kwargs.get('pricing_location')
        self.yield30_day = kwargs.get('yield30_day')
        self.proportion_of_risk = kwargs.get('proportion_of_risk')
        self.beta = kwargs.get('beta')
        self.upfront_payment_date = kwargs.get('upfront_payment_date')
        self.long_exposure = kwargs.get('long_exposure')
        self.tcm_cost_participation_rate20_pct = kwargs.get('tcm_cost_participation_rate20_pct')
        self.multi_asset_class_swap = kwargs.get('multi_asset_class_swap')
        self.idea_status = kwargs.get('idea_status')
        self.contract_subtype = kwargs.get('contract_subtype')
        self.fx_forecast = kwargs.get('fx_forecast')
        self.fixing_time_label = kwargs.get('fixing_time_label')
        self.implementation_id = kwargs.get('implementation_id')
        self.fill_id = kwargs.get('fill_id')
        self.excess_returns = kwargs.get('excess_returns')
        self.dollar_return = kwargs.get('dollar_return')
        self.es_numeric_score = kwargs.get('es_numeric_score')
        self.in_benchmark = kwargs.get('in_benchmark')
        self.return_on_equity = kwargs.get('return_on_equity')
        self.action_sdr = kwargs.get('action_sdr')
        self.restriction_end_date = kwargs.get('restriction_end_date')
        self.queue_in_lots_description = kwargs.get('queue_in_lots_description')
        self.objective = kwargs.get('objective')
        self.nav_price = kwargs.get('nav_price')
        self.precipitation = kwargs.get('precipitation')
        self.hedge_notional = kwargs.get('hedge_notional')
        self.ask_low = kwargs.get('ask_low')
        self.beta_adjusted_net_exposure = kwargs.get('beta_adjusted_net_exposure')
        self.avg_monthly_yield = kwargs.get('avg_monthly_yield')
        self.period_direction = kwargs.get('period_direction')
        self.earnings_per_share = kwargs.get('earnings_per_share')
        self.strike_percentage = kwargs.get('strike_percentage')
        self.excess_return_price = kwargs.get('excess_return_price')
        self.prev_close_bid = kwargs.get('prev_close_bid')
        self.fx_pnl = kwargs.get('fx_pnl')
        self.tcm_cost_horizon16_day = kwargs.get('tcm_cost_horizon16_day')
        self.settlement_date = kwargs.get('settlement_date')
        self.sales_per_share = kwargs.get('sales_per_share')
        self.unadjusted_close = kwargs.get('unadjusted_close')
        self.loan_date = kwargs.get('loan_date')
        self.lending_sec_id = kwargs.get('lending_sec_id')
        self.equity_theta = kwargs.get('equity_theta')
        self.execution_fee = kwargs.get('execution_fee')
        self.start_date = kwargs.get('start_date')
        self.collateral_percentage_actual = kwargs.get('collateral_percentage_actual')
        self.mixed_swap = kwargs.get('mixed_swap')
        self.snowfall = kwargs.get('snowfall')
        self.mic = kwargs.get('mic')
        self.mid = kwargs.get('mid')
        self.relative_return_ytd = kwargs.get('relative_return_ytd')
        self.long = kwargs.get('long')
        self.region_code = kwargs.get('region_code')
        self.long_weight = kwargs.get('long_weight')
        self.calculation_time = kwargs.get('calculation_time')
        self.average_realized_variance = kwargs.get('average_realized_variance')
        self.financial_returns_score = kwargs.get('financial_returns_score')
        self.year_or_quarter = kwargs.get('year_or_quarter')
        self.settlement_type = kwargs.get('settlement_type')
        self.net_change = kwargs.get('net_change')
        self.non_symbol_dimensions = kwargs.get('non_symbol_dimensions')
        self.leg_two_fixed_payment_currency = kwargs.get('leg_two_fixed_payment_currency')
        self.number_of_underliers = kwargs.get('number_of_underliers')
        self.swap_type = kwargs.get('swap_type')
        self.forecast_type = kwargs.get('forecast_type')
        self.sell_settle_date = kwargs.get('sell_settle_date')
        self.new_ideas_ytd = kwargs.get('new_ideas_ytd')
        self.management_fee = kwargs.get('management_fee')
        self.__open = kwargs.get('open_')
        self.source_id = kwargs.get('source_id')
        self.cusip = kwargs.get('cusip')
        self.idea_activity_time = kwargs.get('idea_activity_time')
        self.touch_spread_score = kwargs.get('touch_spread_score')
        self.spread_option_atm_fwd_rate = kwargs.get('spread_option_atm_fwd_rate')
        self.net_exposure = kwargs.get('net_exposure')
        self.frequency = kwargs.get('frequency')
        self.activity_id = kwargs.get('activity_id')
        self.estimated_impact = kwargs.get('estimated_impact')
        self.loan_spread_bucket = kwargs.get('loan_spread_bucket')
        self.event_description = kwargs.get('event_description')
        self.provide_non_display_tape_a = kwargs.get('provide_non_display_tape_a')
        self.strike_reference = kwargs.get('strike_reference')
        self.details = kwargs.get('details')
        self.provide_non_display_tape_c = kwargs.get('provide_non_display_tape_c')
        self.asset_count = kwargs.get('asset_count')
        self.provide_non_display_tape_b = kwargs.get('provide_non_display_tape_b')
        self.sector = kwargs.get('sector')
        self.fundamental_metric = kwargs.get('fundamental_metric')
        self.absolute_value = kwargs.get('absolute_value')
        self.closing_report = kwargs.get('closing_report')
        self.mctr = kwargs.get('mctr')
        self.historical_close = kwargs.get('historical_close')
        self.asset_count_priced = kwargs.get('asset_count_priced')
        self.idea_id = kwargs.get('idea_id')
        self.comment_status = kwargs.get('comment_status')
        self.marginal_cost = kwargs.get('marginal_cost')
        self.settlement_currency = kwargs.get('settlement_currency')
        self.indication_of_collateralization = kwargs.get('indication_of_collateralization')
        self.liq_wkly = kwargs.get('liq_wkly')
        self.lending_partner_fee = kwargs.get('lending_partner_fee')
        self.region = kwargs.get('region')
        self.option_premium = kwargs.get('option_premium')
        self.owner_name = kwargs.get('owner_name')
        self.last_updated_by_id = kwargs.get('last_updated_by_id')
        self.z_score = kwargs.get('z_score')
        self.legal_entity_acct = kwargs.get('legal_entity_acct')
        self.target_shareholder_meeting_date = kwargs.get('target_shareholder_meeting_date')
        self.event_start_time = kwargs.get('event_start_time')
        self.turnover = kwargs.get('turnover')
        self.price_spot_target_unit = kwargs.get('price_spot_target_unit')
        self.compliance_effective_time = kwargs.get('compliance_effective_time')
        self.expiration_date = kwargs.get('expiration_date')
        self.leg_one_type = kwargs.get('leg_one_type')
        self.leg_two_spread = kwargs.get('leg_two_spread')
        self.coverage = kwargs.get('coverage')
        self.g_percentile = kwargs.get('g_percentile')
        self.lending_fund_nav = kwargs.get('lending_fund_nav')
        self.source_original_category = kwargs.get('source_original_category')
        self.composite5_day_adv = kwargs.get('composite5_day_adv')
        self.marginal_contribution_to_risk = kwargs.get('marginal_contribution_to_risk')
        self.latest_execution_time = kwargs.get('latest_execution_time')
        self.close_date = kwargs.get('close_date')
        self.new_ideas_wtd = kwargs.get('new_ideas_wtd')
        self.asset_class_sdr = kwargs.get('asset_class_sdr')
        self.comment = kwargs.get('comment')
        self.source_symbol = kwargs.get('source_symbol')
        self.scenario_id = kwargs.get('scenario_id')
        self.ask_unadjusted = kwargs.get('ask_unadjusted')
        self.termination_tenor = kwargs.get('termination_tenor')
        self.queue_clock_time = kwargs.get('queue_clock_time')
        self.restrict_external_derived_data = kwargs.get('restrict_external_derived_data')
        self.ask_change = kwargs.get('ask_change')
        self.tcm_cost_participation_rate50_pct = kwargs.get('tcm_cost_participation_rate50_pct')
        self.end_date = kwargs.get('end_date')
        self.contract_type = kwargs.get('contract_type')
        self.__type = kwargs.get('type_')
        self.strike_ref = kwargs.get('strike_ref')
        self.cumulative_pnl = kwargs.get('cumulative_pnl')
        self.loss = kwargs.get('loss')
        self.unadjusted_volume = kwargs.get('unadjusted_volume')
        self.midcurve_vol = kwargs.get('midcurve_vol')
        self.trading_cost_pnl = kwargs.get('trading_cost_pnl')
        self.price_notation_type = kwargs.get('price_notation_type')
        self.payment_quantity = kwargs.get('payment_quantity')
        self.position_idx = kwargs.get('position_idx')
        self.implied_volatility_by_relative_strike = kwargs.get('implied_volatility_by_relative_strike')
        self.percent_adv = kwargs.get('percent_adv')
        self.sub_region = kwargs.get('sub_region')
        self.contract = kwargs.get('contract')
        self.payment_frequency1 = kwargs.get('payment_frequency1')
        self.payment_frequency2 = kwargs.get('payment_frequency2')
        self.bespoke = kwargs.get('bespoke')
        self.repo_tenor = kwargs.get('repo_tenor')
        self.quality_stars = kwargs.get('quality_stars')
        self.source_ticker = kwargs.get('source_ticker')
        self.lending_fund = kwargs.get('lending_fund')
        self.tcm_cost_participation_rate15_pct = kwargs.get('tcm_cost_participation_rate15_pct')
        self.sensitivity = kwargs.get('sensitivity')
        self.fiscal_year = kwargs.get('fiscal_year')
        self.recall_date = kwargs.get('recall_date')
        self.internal = kwargs.get('internal')
        self.adjusted_bid_price = kwargs.get('adjusted_bid_price')
        self.var_swap = kwargs.get('var_swap')
        self.fixed_payment_leg2 = kwargs.get('fixed_payment_leg2')
        self.fixed_payment_leg1 = kwargs.get('fixed_payment_leg1')
        self.low_unadjusted = kwargs.get('low_unadjusted')
        self.original_dissemination_id = kwargs.get('original_dissemination_id')
        self.macs_secondary_asset_class = kwargs.get('macs_secondary_asset_class')
        self.leg_two_averaging_method = kwargs.get('leg_two_averaging_method')
        self.sectors_raw = kwargs.get('sectors_raw')
        self.shareclass_price = kwargs.get('shareclass_price')
        self.integrated_score = kwargs.get('integrated_score')
        self.trade_size = kwargs.get('trade_size')
        self.price_spot_entry_value = kwargs.get('price_spot_entry_value')
        self.symbol_dimensions = kwargs.get('symbol_dimensions')
        self.index_location_leg1 = kwargs.get('index_location_leg1')
        self.index_location_leg2 = kwargs.get('index_location_leg2')
        self.option_type_sdr = kwargs.get('option_type_sdr')
        self.scenario_group_id = kwargs.get('scenario_group_id')
        self.avg_yield7_day = kwargs.get('avg_yield7_day')
        self.average_implied_variance = kwargs.get('average_implied_variance')
        self.averaging_method_leg2 = kwargs.get('averaging_method_leg2')
        self.avg_trade_rate_description = kwargs.get('avg_trade_rate_description')
        self.averaging_method_leg1 = kwargs.get('averaging_method_leg1')
        self.fraction = kwargs.get('fraction')
        self.asset_count_short = kwargs.get('asset_count_short')
        self.collateral_percentage_required = kwargs.get('collateral_percentage_required')
        self.opening_auction = kwargs.get('opening_auction')
        self.date = kwargs.get('date')
        self.total_std_return_since_inception = kwargs.get('total_std_return_since_inception')
        self.high_unadjusted = kwargs.get('high_unadjusted')
        self.source_category = kwargs.get('source_category')
        self.tv_product_mnemonic = kwargs.get('tv_product_mnemonic')
        self.volume_unadjusted = kwargs.get('volume_unadjusted')
        self.price_to_earnings = kwargs.get('price_to_earnings')
        self.avg_trade_rate_label = kwargs.get('avg_trade_rate_label')
        self.ann_yield3_month = kwargs.get('ann_yield3_month')
        self.net_flow_std = kwargs.get('net_flow_std')
        self.ask_size = kwargs.get('ask_size')
        self.std30_days_unsubsidized_yield = kwargs.get('std30_days_unsubsidized_yield')
        self.resource = kwargs.get('resource')
        self.dissemination_time = kwargs.get('dissemination_time')
        self.price_to_cash = kwargs.get('price_to_cash')
        self.average_realized_volatility = kwargs.get('average_realized_volatility')
        self.nav_spread = kwargs.get('nav_spread')
        self.bid_price = kwargs.get('bid_price')
        self.dollar_total_return = kwargs.get('dollar_total_return')
        self.block_unit = kwargs.get('block_unit')
        self.es_numeric_percentile = kwargs.get('es_numeric_percentile')
        self.repurchase_rate = kwargs.get('repurchase_rate')
        self.csa_terms = kwargs.get('csa_terms')
        self.daily_net_shareholder_flows = kwargs.get('daily_net_shareholder_flows')
        self.ask_gspread = kwargs.get('ask_gspread')
        self.cal_spread_mis_pricing = kwargs.get('cal_spread_mis_pricing')
        self.leg_two_type = kwargs.get('leg_two_type')
        self.rate366 = kwargs.get('rate366')
        self.rate365 = kwargs.get('rate365')
        self.rate360 = kwargs.get('rate360')
        self.delivery_point_leg1 = kwargs.get('delivery_point_leg1')
        self.opening_report = kwargs.get('opening_report')
        self.value = kwargs.get('value')
        self.leg_one_index_location = kwargs.get('leg_one_index_location')
        self.product_type = kwargs.get('product_type')
        self.quantity = kwargs.get('quantity')
        self.report_id = kwargs.get('report_id')
        self.macs_primary_asset_class = kwargs.get('macs_primary_asset_class')
        self.midcurve_atm_fwd_rate = kwargs.get('midcurve_atm_fwd_rate')
        self.trader = kwargs.get('trader')
        self.equity_risk_premium_index = kwargs.get('equity_risk_premium_index')
        self.clearing_house = kwargs.get('clearing_house')
        self.valuation_date = kwargs.get('valuation_date')
        self.restrict_gs_federation = kwargs.get('restrict_gs_federation')
        self.tcm_cost_horizon6_hour = kwargs.get('tcm_cost_horizon6_hour')
        self.liq_dly = kwargs.get('liq_dly')
        self.price_to_book = kwargs.get('price_to_book')
        self.isin = kwargs.get('isin')

    @property
    def collateral_value_variance(self) -> float:
        """Diffrence between actual and required collateral levels."""
        return self.__collateral_value_variance

    @collateral_value_variance.setter
    def collateral_value_variance(self, value: float):
        self._property_changed('collateral_value_variance')
        self.__collateral_value_variance = value        

    @property
    def year(self) -> str:
        """Year of forecast."""
        return self.__year

    @year.setter
    def year(self, value: str):
        self._property_changed('year')
        self.__year = value        

    @property
    def investment_rate(self) -> float:
        """The rate of return on an investment.  In the context of securities lending, it
           is the rate being earned on the reinvested collateral received from
           the borrower."""
        return self.__investment_rate

    @investment_rate.setter
    def investment_rate(self, value: float):
        self._property_changed('investment_rate')
        self.__investment_rate = value        

    @property
    def forecast_period(self) -> str:
        """Year, quarter or horizon for which the forecast holds."""
        return self.__forecast_period

    @forecast_period.setter
    def forecast_period(self, value: str):
        self._property_changed('forecast_period')
        self.__forecast_period = value        

    @property
    def data_set_ids(self) -> Tuple[Tuple[str, ...], ...]:
        """The dataset Ids."""
        return self.__data_set_ids

    @data_set_ids.setter
    def data_set_ids(self, value: Tuple[Tuple[str, ...], ...]):
        self._property_changed('data_set_ids')
        self.__data_set_ids = value        

    @property
    def bid_unadjusted(self) -> float:
        """Unadjusted bid level of an asset based on official exchange fixing or
           calculation agent marked level."""
        return self.__bid_unadjusted

    @bid_unadjusted.setter
    def bid_unadjusted(self, value: float):
        self._property_changed('bid_unadjusted')
        self.__bid_unadjusted = value        

    @property
    def client_type(self) -> str:
        """Client type, ex: Hedge Fund, Real Money, Corporate, etc."""
        return self.__client_type

    @client_type.setter
    def client_type(self, value: str):
        self._property_changed('client_type')
        self.__client_type = value        

    @property
    def available_inventory(self) -> float:
        """An estimated indication of the share quantity potentially available to borrow in
           the relevant asset."""
        return self.__available_inventory

    @available_inventory.setter
    def available_inventory(self, value: float):
        self._property_changed('available_inventory')
        self.__available_inventory = value        

    @property
    def est1_day_complete_pct(self) -> float:
        """Estimated 1 day completion percentage."""
        return self.__est1_day_complete_pct

    @est1_day_complete_pct.setter
    def est1_day_complete_pct(self, value: float):
        self._property_changed('est1_day_complete_pct')
        self.__est1_day_complete_pct = value        

    @property
    def created_by_id(self) -> str:
        """Unique identifier of user who created the object"""
        return self.__created_by_id

    @created_by_id.setter
    def created_by_id(self, value: str):
        self._property_changed('created_by_id')
        self.__created_by_id = value        

    @property
    def vehicle_type(self) -> str:
        """Type of investment vehicle. Only viewable after having been granted additional
           access to asset information."""
        return self.__vehicle_type

    @vehicle_type.setter
    def vehicle_type(self, value: str):
        self._property_changed('vehicle_type')
        self.__vehicle_type = value        

    @property
    def daily_risk(self) -> float:
        """Daily Risk Value."""
        return self.__daily_risk

    @daily_risk.setter
    def daily_risk(self, value: float):
        self._property_changed('daily_risk')
        self.__daily_risk = value        

    @property
    def energy(self) -> float:
        """Energy price component."""
        return self.__energy

    @energy.setter
    def energy(self, value: float):
        self._property_changed('energy')
        self.__energy = value        

    @property
    def market_data_type(self) -> str:
        """The market data type (e.g. IR_BASIS, FX_Vol). This can be resolved into a
           dataset when combined with vendor and intraday=true/false."""
        return self.__market_data_type

    @market_data_type.setter
    def market_data_type(self, value: str):
        self._property_changed('market_data_type')
        self.__market_data_type = value        

    @property
    def real_short_rates_contribution(self) -> float:
        """Contribution of short rate component to real FCI."""
        return self.__real_short_rates_contribution

    @real_short_rates_contribution.setter
    def real_short_rates_contribution(self, value: float):
        self._property_changed('real_short_rates_contribution')
        self.__real_short_rates_contribution = value        

    @property
    def sentiment_score(self) -> float:
        """A value representing a sentiment indicator."""
        return self.__sentiment_score

    @sentiment_score.setter
    def sentiment_score(self, value: float):
        self._property_changed('sentiment_score')
        self.__sentiment_score = value        

    @property
    def leg_one_payment_type(self) -> str:
        """Type of payment stream."""
        return self.__leg_one_payment_type

    @leg_one_payment_type.setter
    def leg_one_payment_type(self, value: str):
        self._property_changed('leg_one_payment_type')
        self.__leg_one_payment_type = value        

    @property
    def provide_tape_c(self) -> float:
        """Goldman's rate for liquidity providing trades on tape C."""
        return self.__provide_tape_c

    @provide_tape_c.setter
    def provide_tape_c(self, value: float):
        self._property_changed('provide_tape_c')
        self.__provide_tape_c = value        

    @property
    def value_previous(self) -> str:
        """Value for the previous period after the revision (if revision is applicable)."""
        return self.__value_previous

    @value_previous.setter
    def value_previous(self, value: str):
        self._property_changed('value_previous')
        self.__value_previous = value        

    @property
    def delivery_point_leg2(self) -> str:
        """Delivery point of leg."""
        return self.__delivery_point_leg2

    @delivery_point_leg2.setter
    def delivery_point_leg2(self, value: str):
        self._property_changed('delivery_point_leg2')
        self.__delivery_point_leg2 = value        

    @property
    def avg_trade_rate(self) -> float:
        """The Average Trading Rate of the stock on the particular date."""
        return self.__avg_trade_rate

    @avg_trade_rate.setter
    def avg_trade_rate(self, value: float):
        self._property_changed('avg_trade_rate')
        self.__avg_trade_rate = value        

    @property
    def short_level(self) -> float:
        """Level of the 5-day normalized flow for short selling/covering."""
        return self.__short_level

    @short_level.setter
    def short_level(self, value: float):
        self._property_changed('short_level')
        self.__short_level = value        

    @property
    def version(self) -> float:
        """Version number."""
        return self.__version

    @version.setter
    def version(self, value: float):
        self._property_changed('version')
        self.__version = value        

    @property
    def policy_rate_expectation(self) -> float:
        """Returns the historical policy rate expectations for a given meeting date."""
        return self.__policy_rate_expectation

    @policy_rate_expectation.setter
    def policy_rate_expectation(self, value: float):
        self._property_changed('policy_rate_expectation')
        self.__policy_rate_expectation = value        

    @property
    def exposure(self) -> float:
        """Exposure of a given asset or portfolio in the denominated currency of the asset
           or portfolio."""
        return self.__exposure

    @exposure.setter
    def exposure(self, value: float):
        self._property_changed('exposure')
        self.__exposure = value        

    @property
    def market_data_asset(self) -> str:
        """The market data asset (e.g. USD, USD/EUR)."""
        return self.__market_data_asset

    @market_data_asset.setter
    def market_data_asset(self, value: str):
        self._property_changed('market_data_asset')
        self.__market_data_asset = value        

    @property
    def earnings_per_share_positive(self) -> float:
        """Earnings per share positive."""
        return self.__earnings_per_share_positive

    @earnings_per_share_positive.setter
    def earnings_per_share_positive(self, value: float):
        self._property_changed('earnings_per_share_positive')
        self.__earnings_per_share_positive = value        

    @property
    def unadjusted_high(self) -> float:
        """Unadjusted high level of an asset based on official exchange fixing or
           calculation agent marked level."""
        return self.__unadjusted_high

    @unadjusted_high.setter
    def unadjusted_high(self, value: float):
        self._property_changed('unadjusted_high')
        self.__unadjusted_high = value        

    @property
    def source_importance(self) -> float:
        """Source importance."""
        return self.__source_importance

    @source_importance.setter
    def source_importance(self, value: float):
        self._property_changed('source_importance')
        self.__source_importance = value        

    @property
    def relative_return_qtd(self) -> float:
        """Relative Return Quarter to Date."""
        return self.__relative_return_qtd

    @relative_return_qtd.setter
    def relative_return_qtd(self, value: float):
        self._property_changed('relative_return_qtd')
        self.__relative_return_qtd = value        

    @property
    def minutes_to_trade100_pct(self) -> float:
        """Minutes to trade 100 percent."""
        return self.__minutes_to_trade100_pct

    @minutes_to_trade100_pct.setter
    def minutes_to_trade100_pct(self, value: float):
        self._property_changed('minutes_to_trade100_pct')
        self.__minutes_to_trade100_pct = value        

    @property
    def expiration_tenor(self) -> str:
        """Tenor"""
        return self.__expiration_tenor

    @expiration_tenor.setter
    def expiration_tenor(self, value: str):
        self._property_changed('expiration_tenor')
        self.__expiration_tenor = value        

    @property
    def market_model_id(self) -> str:
        """Marquee unique market model identifier"""
        return self.__market_model_id

    @market_model_id.setter
    def market_model_id(self, value: str):
        self._property_changed('market_model_id')
        self.__market_model_id = value        

    @property
    def realized_correlation(self) -> float:
        """Correlation of an asset realized by observations of market prices."""
        return self.__realized_correlation

    @realized_correlation.setter
    def realized_correlation(self, value: float):
        self._property_changed('realized_correlation')
        self.__realized_correlation = value        

    @property
    def collateral_value_actual(self) -> float:
        """Value of collateral covering the given position."""
        return self.__collateral_value_actual

    @collateral_value_actual.setter
    def collateral_value_actual(self, value: float):
        self._property_changed('collateral_value_actual')
        self.__collateral_value_actual = value        

    @property
    def upfront_payment(self) -> float:
        """Upfront payment fee."""
        return self.__upfront_payment

    @upfront_payment.setter
    def upfront_payment(self, value: float):
        self._property_changed('upfront_payment')
        self.__upfront_payment = value        

    @property
    def atm_fwd_rate(self) -> float:
        """ATM forward rate."""
        return self.__atm_fwd_rate

    @atm_fwd_rate.setter
    def atm_fwd_rate(self, value: float):
        self._property_changed('atm_fwd_rate')
        self.__atm_fwd_rate = value        

    @property
    def provide_tape_a(self) -> float:
        """Goldman's rate for liquidity providing trades on tape A."""
        return self.__provide_tape_a

    @provide_tape_a.setter
    def provide_tape_a(self, value: float):
        self._property_changed('provide_tape_a')
        self.__provide_tape_a = value        

    @property
    def provide_tape_b(self) -> float:
        """Goldman's rate for liquidity providing trades on tape B."""
        return self.__provide_tape_b

    @provide_tape_b.setter
    def provide_tape_b(self, value: float):
        self._property_changed('provide_tape_b')
        self.__provide_tape_b = value        

    @property
    def tcm_cost_participation_rate75_pct(self) -> float:
        """TCM cost with a 75 percent participation rate."""
        return self.__tcm_cost_participation_rate75_pct

    @tcm_cost_participation_rate75_pct.setter
    def tcm_cost_participation_rate75_pct(self, value: float):
        self._property_changed('tcm_cost_participation_rate75_pct')
        self.__tcm_cost_participation_rate75_pct = value        

    @property
    def close(self) -> float:
        """Closing level of an asset based on official exchange fixing or calculation agent
           marked level."""
        return self.__close

    @close.setter
    def close(self, value: float):
        self._property_changed('close')
        self.__close = value        

    @property
    def a(self) -> float:
        """Stock specific coefficient."""
        return self.__a

    @a.setter
    def a(self, value: float):
        self._property_changed('a')
        self.__a = value        

    @property
    def b(self) -> float:
        """Stock specific coefficient."""
        return self.__b

    @b.setter
    def b(self, value: float):
        self._property_changed('b')
        self.__b = value        

    @property
    def c(self) -> float:
        """Stock specific coefficient."""
        return self.__c

    @c.setter
    def c(self, value: float):
        self._property_changed('c')
        self.__c = value        

    @property
    def equity_vega(self) -> float:
        """Vega exposure to equity products."""
        return self.__equity_vega

    @equity_vega.setter
    def equity_vega(self, value: float):
        self._property_changed('equity_vega')
        self.__equity_vega = value        

    @property
    def leg_one_spread(self) -> float:
        """Spread of leg."""
        return self.__leg_one_spread

    @leg_one_spread.setter
    def leg_one_spread(self, value: float):
        self._property_changed('leg_one_spread')
        self.__leg_one_spread = value        

    @property
    def lender_payment(self) -> float:
        """Payment made to lender's bank in support of the income accrued from securities
           lending."""
        return self.__lender_payment

    @lender_payment.setter
    def lender_payment(self, value: float):
        self._property_changed('lender_payment')
        self.__lender_payment = value        

    @property
    def five_day_move(self) -> float:
        """Five day move in the price."""
        return self.__five_day_move

    @five_day_move.setter
    def five_day_move(self, value: float):
        self._property_changed('five_day_move')
        self.__five_day_move = value        

    @property
    def geography_name(self) -> str:
        """Name of the country or region for which FCI is calculated. Region names are
           Developed Markets, Emerging Markets, Euro Area, Global."""
        return self.__geography_name

    @geography_name.setter
    def geography_name(self, value: str):
        self._property_changed('geography_name')
        self.__geography_name = value        

    @property
    def borrower(self) -> str:
        """Name of the borrowing entity on a securities lending agreement."""
        return self.__borrower

    @borrower.setter
    def borrower(self, value: str):
        self._property_changed('borrower')
        self.__borrower = value        

    @property
    def value_format(self) -> float:
        """Value format."""
        return self.__value_format

    @value_format.setter
    def value_format(self, value: float):
        self._property_changed('value_format')
        self.__value_format = value        

    @property
    def performance_contribution(self) -> float:
        """The contribution of an underlying asset to the overall performance."""
        return self.__performance_contribution

    @performance_contribution.setter
    def performance_contribution(self, value: float):
        self._property_changed('performance_contribution')
        self.__performance_contribution = value        

    @property
    def target_notional(self) -> float:
        """Notional value of the hedge target."""
        return self.__target_notional

    @target_notional.setter
    def target_notional(self, value: float):
        self._property_changed('target_notional')
        self.__target_notional = value        

    @property
    def fill_leg_id(self) -> str:
        """Unique identifier for the leg on which the fill executed."""
        return self.__fill_leg_id

    @fill_leg_id.setter
    def fill_leg_id(self, value: str):
        self._property_changed('fill_leg_id')
        self.__fill_leg_id = value        

    @property
    def rationale(self) -> str:
        """Reason for changing the status of a trade idea."""
        return self.__rationale

    @rationale.setter
    def rationale(self, value: str):
        self._property_changed('rationale')
        self.__rationale = value        

    @property
    def mkt_class(self) -> str:
        """The MDAPI Class (e.g. Swap, Cash)."""
        return self.__mkt_class

    @mkt_class.setter
    def mkt_class(self, value: str):
        self._property_changed('mkt_class')
        self.__mkt_class = value        

    @property
    def last_updated_since(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__last_updated_since

    @last_updated_since.setter
    def last_updated_since(self, value: datetime.datetime):
        self._property_changed('last_updated_since')
        self.__last_updated_since = value        

    @property
    def equities_contribution(self) -> float:
        """Contribution of equity component to FCI."""
        return self.__equities_contribution

    @equities_contribution.setter
    def equities_contribution(self, value: float):
        self._property_changed('equities_contribution')
        self.__equities_contribution = value        

    @property
    def congestion(self) -> float:
        """Congestion price component."""
        return self.__congestion

    @congestion.setter
    def congestion(self, value: float):
        self._property_changed('congestion')
        self.__congestion = value        

    @property
    def event_category(self) -> str:
        """Category."""
        return self.__event_category

    @event_category.setter
    def event_category(self, value: str):
        self._property_changed('event_category')
        self.__event_category = value        

    @property
    def short_rates_contribution(self) -> float:
        """Contribution of short rate component to FCI."""
        return self.__short_rates_contribution

    @short_rates_contribution.setter
    def short_rates_contribution(self, value: float):
        self._property_changed('short_rates_contribution')
        self.__short_rates_contribution = value        

    @property
    def unadjusted_open(self) -> float:
        """Unadjusted open level of an asset based on official exchange fixing or
           calculation agent marked level."""
        return self.__unadjusted_open

    @unadjusted_open.setter
    def unadjusted_open(self, value: float):
        self._property_changed('unadjusted_open')
        self.__unadjusted_open = value        

    @property
    def criticality(self) -> float:
        """The upgrade criticality of a deployment."""
        return self.__criticality

    @criticality.setter
    def criticality(self, value: float):
        self._property_changed('criticality')
        self.__criticality = value        

    @property
    def mtm_price(self) -> float:
        """Amount of profit or loss realized over statement period."""
        return self.__mtm_price

    @mtm_price.setter
    def mtm_price(self, value: float):
        self._property_changed('mtm_price')
        self.__mtm_price = value        

    @property
    def bid_ask_spread(self) -> float:
        """Bid ask spread."""
        return self.__bid_ask_spread

    @bid_ask_spread.setter
    def bid_ask_spread(self, value: float):
        self._property_changed('bid_ask_spread')
        self.__bid_ask_spread = value        

    @property
    def leg_one_averaging_method(self) -> str:
        """Averaging method of leg."""
        return self.__leg_one_averaging_method

    @leg_one_averaging_method.setter
    def leg_one_averaging_method(self, value: str):
        self._property_changed('leg_one_averaging_method')
        self.__leg_one_averaging_method = value        

    @property
    def option_type(self) -> str:
        """One of two option types."""
        return self.__option_type

    @option_type.setter
    def option_type(self, value: str):
        self._property_changed('option_type')
        self.__option_type = value        

    @property
    def portfolio_assets(self) -> float:
        """Total amount of assets under management across all share classes."""
        return self.__portfolio_assets

    @portfolio_assets.setter
    def portfolio_assets(self, value: float):
        self._property_changed('portfolio_assets')
        self.__portfolio_assets = value        

    @property
    def termination_date(self) -> datetime.date:
        """The date at which the measure becomes terminated."""
        return self.__termination_date

    @termination_date.setter
    def termination_date(self, value: datetime.date):
        self._property_changed('termination_date')
        self.__termination_date = value        

    @property
    def tcm_cost_horizon3_hour(self) -> float:
        """TCM cost with a 3 hour time horizon."""
        return self.__tcm_cost_horizon3_hour

    @tcm_cost_horizon3_hour.setter
    def tcm_cost_horizon3_hour(self, value: float):
        self._property_changed('tcm_cost_horizon3_hour')
        self.__tcm_cost_horizon3_hour = value        

    @property
    def number_covered(self) -> float:
        """Number of underlyers covered by risk model."""
        return self.__number_covered

    @number_covered.setter
    def number_covered(self, value: float):
        self._property_changed('number_covered')
        self.__number_covered = value        

    @property
    def credit_limit(self) -> float:
        """The allowed credit limit."""
        return self.__credit_limit

    @credit_limit.setter
    def credit_limit(self, value: float):
        self._property_changed('credit_limit')
        self.__credit_limit = value        

    @property
    def number_of_positions(self) -> float:
        """Number of positions."""
        return self.__number_of_positions

    @number_of_positions.setter
    def number_of_positions(self, value: float):
        self._property_changed('number_of_positions')
        self.__number_of_positions = value        

    @property
    def effective_tenor(self) -> str:
        """Tenor"""
        return self.__effective_tenor

    @effective_tenor.setter
    def effective_tenor(self, value: str):
        self._property_changed('effective_tenor')
        self.__effective_tenor = value        

    @property
    def open_unadjusted(self) -> float:
        """Unadjusted open level of an asset based on official exchange fixing or
           calculation agent marked level."""
        return self.__open_unadjusted

    @open_unadjusted.setter
    def open_unadjusted(self, value: float):
        self._property_changed('open_unadjusted')
        self.__open_unadjusted = value        

    @property
    def ask_price(self) -> float:
        """Latest Ask Price (price offering to sell)."""
        return self.__ask_price

    @ask_price.setter
    def ask_price(self, value: float):
        self._property_changed('ask_price')
        self.__ask_price = value        

    @property
    def event_id(self) -> str:
        """Goldman Sachs internal event identifier."""
        return self.__event_id

    @event_id.setter
    def event_id(self, value: str):
        self._property_changed('event_id')
        self.__event_id = value        

    @property
    def sectors(self) -> Tuple[str, ...]:
        """Sector classifications of an asset."""
        return self.__sectors

    @sectors.setter
    def sectors(self, value: Tuple[str, ...]):
        self._property_changed('sectors')
        self.__sectors = value        

    @property
    def std30_days_subsidized_yield(self) -> float:
        """Average annual total returns as of most recent calendar quarter-end, does not
           account for any fee waivers or expense reimbursements."""
        return self.__std30_days_subsidized_yield

    @std30_days_subsidized_yield.setter
    def std30_days_subsidized_yield(self, value: float):
        self._property_changed('std30_days_subsidized_yield')
        self.__std30_days_subsidized_yield = value        

    @property
    def annualized_tracking_error(self) -> float:
        """Annualized tracking error."""
        return self.__annualized_tracking_error

    @annualized_tracking_error.setter
    def annualized_tracking_error(self, value: float):
        self._property_changed('annualized_tracking_error')
        self.__annualized_tracking_error = value        

    @property
    def additional_price_notation_type(self) -> str:
        """Basis points, Price, Yield, Spread, Coupon, etc., depending on the type of SB
           swap, which is calculated at affirmation."""
        return self.__additional_price_notation_type

    @additional_price_notation_type.setter
    def additional_price_notation_type(self, value: str):
        self._property_changed('additional_price_notation_type')
        self.__additional_price_notation_type = value        

    @property
    def vol_swap(self) -> float:
        """The strike in volatility terms, calculated as square root of fair variance."""
        return self.__vol_swap

    @vol_swap.setter
    def vol_swap(self, value: float):
        self._property_changed('vol_swap')
        self.__vol_swap = value        

    @property
    def real_fci(self) -> float:
        """Real FCI value."""
        return self.__real_fci

    @real_fci.setter
    def real_fci(self, value: float):
        self._property_changed('real_fci')
        self.__real_fci = value        

    @property
    def annualized_risk(self) -> float:
        """Annualized risk."""
        return self.__annualized_risk

    @annualized_risk.setter
    def annualized_risk(self, value: float):
        self._property_changed('annualized_risk')
        self.__annualized_risk = value        

    @property
    def block_trades_and_large_notional_off_facility_swaps(self) -> str:
        """An indication of whether this is a block trade or off-facility swap."""
        return self.__block_trades_and_large_notional_off_facility_swaps

    @block_trades_and_large_notional_off_facility_swaps.setter
    def block_trades_and_large_notional_off_facility_swaps(self, value: str):
        self._property_changed('block_trades_and_large_notional_off_facility_swaps')
        self.__block_trades_and_large_notional_off_facility_swaps = value        

    @property
    def leg_one_fixed_payment_currency(self) -> str:
        """If fixed payment leg, the unit of fixed payment."""
        return self.__leg_one_fixed_payment_currency

    @leg_one_fixed_payment_currency.setter
    def leg_one_fixed_payment_currency(self, value: str):
        self._property_changed('leg_one_fixed_payment_currency')
        self.__leg_one_fixed_payment_currency = value        

    @property
    def gross_exposure(self) -> float:
        """Sum of absolute long and short exposures in the portfolio. If you are $60 short
           and $40 long, then the grossExposure would be $100 (60+40)."""
        return self.__gross_exposure

    @gross_exposure.setter
    def gross_exposure(self, value: float):
        self._property_changed('gross_exposure')
        self.__gross_exposure = value        

    @property
    def payment_frequency_leg1(self) -> str:
        """An integer multiplier of a time period describing how often the parties to the
           SB swap transaction exchange payments associated with each party???s
           obligation (leg 1). Such payment frequency may be described as one
           letter preceded by an integer."""
        return self.__payment_frequency_leg1

    @payment_frequency_leg1.setter
    def payment_frequency_leg1(self, value: str):
        self._property_changed('payment_frequency_leg1')
        self.__payment_frequency_leg1 = value        

    @property
    def payment_frequency_leg2(self) -> str:
        """An integer multiplier of a time period describing how often the parties to the
           SB swap transaction exchange payments associated with each party???s
           obligation (leg 2). Such payment frequency may be described as one
           letter preceded by an integer."""
        return self.__payment_frequency_leg2

    @payment_frequency_leg2.setter
    def payment_frequency_leg2(self, value: str):
        self._property_changed('payment_frequency_leg2')
        self.__payment_frequency_leg2 = value        

    @property
    def volume_composite(self) -> float:
        """Accumulated number of shares, lots or contracts traded according to the market
           convention at all exchanges."""
        return self.__volume_composite

    @volume_composite.setter
    def volume_composite(self, value: float):
        self._property_changed('volume_composite')
        self.__volume_composite = value        

    @property
    def volume(self) -> float:
        """Accumulated number of shares, lots or contracts traded according to the market
           convention."""
        return self.__volume

    @volume.setter
    def volume(self, value: float):
        self._property_changed('volume')
        self.__volume = value        

    @property
    def adv(self) -> float:
        """Average number of shares or units of a given asset traded over a defined period."""
        return self.__adv

    @adv.setter
    def adv(self, value: float):
        self._property_changed('adv')
        self.__adv = value        

    @property
    def external(self) -> bool:
        """Whether entity was created by an external user."""
        return self.__external

    @external.setter
    def external(self, value: bool):
        self._property_changed('external')
        self.__external = value        

    @property
    def short_conviction_medium(self) -> float:
        """The count of short ideas with medium conviction."""
        return self.__short_conviction_medium

    @short_conviction_medium.setter
    def short_conviction_medium(self, value: float):
        self._property_changed('short_conviction_medium')
        self.__short_conviction_medium = value        

    @property
    def exchange(self) -> str:
        """Name of marketplace where security, derivative or other instrument is traded"""
        return self.__exchange

    @exchange.setter
    def exchange(self, value: str):
        self._property_changed('exchange')
        self.__exchange = value        

    @property
    def trade_price(self) -> float:
        """Last trade price or value."""
        return self.__trade_price

    @trade_price.setter
    def trade_price(self, value: float):
        self._property_changed('trade_price')
        self.__trade_price = value        

    @property
    def cleared(self) -> str:
        """An indication of whether or not an SB swap transaction is going to be cleared by
           a derivatives clearing organization."""
        return self.__cleared

    @cleared.setter
    def cleared(self, value: str):
        self._property_changed('cleared')
        self.__cleared = value        

    @property
    def es_policy_score(self) -> float:
        """Score for E&S policy metrics."""
        return self.__es_policy_score

    @es_policy_score.setter
    def es_policy_score(self, value: float):
        self._property_changed('es_policy_score')
        self.__es_policy_score = value        

    @property
    def prime_id_numeric(self) -> float:
        """Prime ID as a number."""
        return self.__prime_id_numeric

    @prime_id_numeric.setter
    def prime_id_numeric(self, value: float):
        self._property_changed('prime_id_numeric')
        self.__prime_id_numeric = value        

    @property
    def leg_one_index(self) -> str:
        """If floating index leg, the index."""
        return self.__leg_one_index

    @leg_one_index.setter
    def leg_one_index(self, value: str):
        self._property_changed('leg_one_index')
        self.__leg_one_index = value        

    @property
    def on_loan_percentage(self) -> float:
        """On loan ratio as compared net asset value of lending fund."""
        return self.__on_loan_percentage

    @on_loan_percentage.setter
    def on_loan_percentage(self, value: float):
        self._property_changed('on_loan_percentage')
        self.__on_loan_percentage = value        

    @property
    def bid_high(self) -> float:
        """The highest bid (price willing to buy)."""
        return self.__bid_high

    @bid_high.setter
    def bid_high(self, value: float):
        self._property_changed('bid_high')
        self.__bid_high = value        

    @property
    def fair_variance(self) -> float:
        """Strike such that the price of an uncapped variance swap on the underlying index
           is zero at inception."""
        return self.__fair_variance

    @fair_variance.setter
    def fair_variance(self, value: float):
        self._property_changed('fair_variance')
        self.__fair_variance = value        

    @property
    def hit_rate_wtd(self) -> float:
        """Hit Rate Ratio Week to Date."""
        return self.__hit_rate_wtd

    @hit_rate_wtd.setter
    def hit_rate_wtd(self, value: float):
        self._property_changed('hit_rate_wtd')
        self.__hit_rate_wtd = value        

    @property
    def bos_in_bps_description(self) -> str:
        """Description of the Stock's Bid-Offer Spread in Basis points on the particular
           date."""
        return self.__bos_in_bps_description

    @bos_in_bps_description.setter
    def bos_in_bps_description(self, value: str):
        self._property_changed('bos_in_bps_description')
        self.__bos_in_bps_description = value        

    @property
    def low_price(self) -> float:
        """Low level of an asset based on official exchange fixing or calculation agent
           marked level."""
        return self.__low_price

    @low_price.setter
    def low_price(self, value: float):
        self._property_changed('low_price')
        self.__low_price = value        

    @property
    def realized_volatility(self) -> float:
        """Volatility of an asset realized by observations of market prices."""
        return self.__realized_volatility

    @realized_volatility.setter
    def realized_volatility(self, value: float):
        self._property_changed('realized_volatility')
        self.__realized_volatility = value        

    @property
    def adv22_day_pct(self) -> float:
        """Median number of shares or units of a given asset traded over a 21 day period."""
        return self.__adv22_day_pct

    @adv22_day_pct.setter
    def adv22_day_pct(self, value: float):
        self._property_changed('adv22_day_pct')
        self.__adv22_day_pct = value        

    @property
    def clone_parent_id(self) -> str:
        """Marquee unique identifier"""
        return self.__clone_parent_id

    @clone_parent_id.setter
    def clone_parent_id(self, value: str):
        self._property_changed('clone_parent_id')
        self.__clone_parent_id = value        

    @property
    def price_range_in_ticks_label(self):
        return self.__price_range_in_ticks_label

    @price_range_in_ticks_label.setter
    def price_range_in_ticks_label(self, value):
        self._property_changed('price_range_in_ticks_label')
        self.__price_range_in_ticks_label = value        

    @property
    def ticker(self) -> str:
        """Ticker."""
        return self.__ticker

    @ticker.setter
    def ticker(self, value: str):
        self._property_changed('ticker')
        self.__ticker = value        

    @property
    def tcm_cost_horizon1_day(self) -> float:
        """TCM cost with a 1 day time horizon."""
        return self.__tcm_cost_horizon1_day

    @tcm_cost_horizon1_day.setter
    def tcm_cost_horizon1_day(self, value: float):
        self._property_changed('tcm_cost_horizon1_day')
        self.__tcm_cost_horizon1_day = value        

    @property
    def approval(self) -> float:
        """Approval rating."""
        return self.__approval

    @approval.setter
    def approval(self, value: float):
        self._property_changed('approval')
        self.__approval = value        

    @property
    def file_location(self) -> str:
        return self.__file_location

    @file_location.setter
    def file_location(self, value: str):
        self._property_changed('file_location')
        self.__file_location = value        

    @property
    def leg_two_payment_type(self) -> str:
        """Type of payment stream."""
        return self.__leg_two_payment_type

    @leg_two_payment_type.setter
    def leg_two_payment_type(self, value: str):
        self._property_changed('leg_two_payment_type')
        self.__leg_two_payment_type = value        

    @property
    def horizon(self) -> str:
        """Time period indicating the validity of the idea. Eg. 2d (2 days), 1w (1 week),
           3m (3 months), 1y (1 year)."""
        return self.__horizon

    @horizon.setter
    def horizon(self, value: str):
        self._property_changed('horizon')
        self.__horizon = value        

    @property
    def day_count_convention_leg1(self) -> str:
        """The determination of how interest accrues over time for the SB swap."""
        return self.__day_count_convention_leg1

    @day_count_convention_leg1.setter
    def day_count_convention_leg1(self, value: str):
        self._property_changed('day_count_convention_leg1')
        self.__day_count_convention_leg1 = value        

    @property
    def source_value_forecast(self) -> str:
        """TE own projections."""
        return self.__source_value_forecast

    @source_value_forecast.setter
    def source_value_forecast(self, value: str):
        self._property_changed('source_value_forecast')
        self.__source_value_forecast = value        

    @property
    def short_conviction_large(self) -> float:
        """The count of short ideas with large conviction."""
        return self.__short_conviction_large

    @short_conviction_large.setter
    def short_conviction_large(self, value: float):
        self._property_changed('short_conviction_large')
        self.__short_conviction_large = value        

    @property
    def day_count_convention_leg2(self) -> str:
        """Day count convention for leg 2."""
        return self.__day_count_convention_leg2

    @day_count_convention_leg2.setter
    def day_count_convention_leg2(self, value: str):
        self._property_changed('day_count_convention_leg2')
        self.__day_count_convention_leg2 = value        

    @property
    def counter_party_status(self) -> str:
        """The lending status of a counterparty for a particular portfolio."""
        return self.__counter_party_status

    @counter_party_status.setter
    def counter_party_status(self, value: str):
        self._property_changed('counter_party_status')
        self.__counter_party_status = value        

    @property
    def composite22_day_adv(self) -> float:
        """Composite 22 day ADV."""
        return self.__composite22_day_adv

    @composite22_day_adv.setter
    def composite22_day_adv(self, value: float):
        self._property_changed('composite22_day_adv')
        self.__composite22_day_adv = value        

    @property
    def dollar_excess_return(self) -> float:
        """The dollar excess return of an instrument."""
        return self.__dollar_excess_return

    @dollar_excess_return.setter
    def dollar_excess_return(self, value: float):
        self._property_changed('dollar_excess_return')
        self.__dollar_excess_return = value        

    @property
    def trade_end_date(self) -> datetime.date:
        """End date of the trade."""
        return self.__trade_end_date

    @trade_end_date.setter
    def trade_end_date(self, value: datetime.date):
        self._property_changed('trade_end_date')
        self.__trade_end_date = value        

    @property
    def percent_of_mediandv1m(self) -> float:
        """Percentage of median daily volume calculated using 1 month period (last 22
           trading days)."""
        return self.__percent_of_mediandv1m

    @percent_of_mediandv1m.setter
    def percent_of_mediandv1m(self, value: float):
        self._property_changed('percent_of_mediandv1m')
        self.__percent_of_mediandv1m = value        

    @property
    def lendables(self) -> float:
        """Market value of holdings available to a securities lending program for lending."""
        return self.__lendables

    @lendables.setter
    def lendables(self, value: float):
        self._property_changed('lendables')
        self.__lendables = value        

    @property
    def loan_spread_required(self) -> float:
        """The minimum spread requirement for a securities lending loan."""
        return self.__loan_spread_required

    @loan_spread_required.setter
    def loan_spread_required(self, value: float):
        self._property_changed('loan_spread_required')
        self.__loan_spread_required = value        

    @property
    def asset_class(self) -> str:
        """Asset classification of security. Assets are classified into broad groups which
           exhibit similar characteristics and behave in a consistent way under
           different market conditions"""
        return self.__asset_class

    @asset_class.setter
    def asset_class(self, value: str):
        self._property_changed('asset_class')
        self.__asset_class = value        

    @property
    def sovereign_spread_contribution(self) -> float:
        """Contribution of sovereign spread component to FCI. Only applicable to Euro
           countries."""
        return self.__sovereign_spread_contribution

    @sovereign_spread_contribution.setter
    def sovereign_spread_contribution(self, value: float):
        self._property_changed('sovereign_spread_contribution')
        self.__sovereign_spread_contribution = value        

    @property
    def bos_in_ticks_label(self):
        return self.__bos_in_ticks_label

    @bos_in_ticks_label.setter
    def bos_in_ticks_label(self, value):
        self._property_changed('bos_in_ticks_label')
        self.__bos_in_ticks_label = value        

    @property
    def ric(self) -> str:
        """Reuters instrument code (subject to licensing)."""
        return self.__ric

    @ric.setter
    def ric(self, value: str):
        self._property_changed('ric')
        self.__ric = value        

    @property
    def position_source_id(self) -> str:
        """Marquee unique identifier"""
        return self.__position_source_id

    @position_source_id.setter
    def position_source_id(self, value: str):
        self._property_changed('position_source_id')
        self.__position_source_id = value        

    @property
    def rate_type(self) -> str:
        """Type of swap structured for a Central Bank swap: rate type = Meeting Forward,
           swaps structured trough End of Year, rateType = EOY Forward and for
           Spot OIS value rateType = Spot."""
        return self.__rate_type

    @rate_type.setter
    def rate_type(self, value: str):
        self._property_changed('rate_type')
        self.__rate_type = value        

    @property
    def gs_sustain_region(self) -> str:
        """Region assigned by GIR ESG SUSTAIN team."""
        return self.__gs_sustain_region

    @gs_sustain_region.setter
    def gs_sustain_region(self, value: str):
        self._property_changed('gs_sustain_region')
        self.__gs_sustain_region = value        

    @property
    def deployment_id(self) -> float:
        """Deployment ID."""
        return self.__deployment_id

    @deployment_id.setter
    def deployment_id(self, value: float):
        self._property_changed('deployment_id')
        self.__deployment_id = value        

    @property
    def loan_status(self) -> str:
        """Notes which point of the lifecyle a securities lending loan is in."""
        return self.__loan_status

    @loan_status.setter
    def loan_status(self, value: str):
        self._property_changed('loan_status')
        self.__loan_status = value        

    @property
    def short_weight(self) -> float:
        """Short weight of a position in a given portfolio. Equivalent to position short
           exposure / total short exposure. If you have a position with a
           shortExposure of $20, and your portfolio shortExposure is $100, then
           your asset shortWeight would be 0.2 (20/100)."""
        return self.__short_weight

    @short_weight.setter
    def short_weight(self, value: float):
        self._property_changed('short_weight')
        self.__short_weight = value        

    @property
    def geography_id(self) -> str:
        """Two-digit code for countries and regions for which FCI numbers are represented.
           For countries it is the ISO 3166 2-digit country code. Regions are
           denoted as DM (Developed Markets), EM (Emerging Markets), EA (Euro
           Area) and GL (Global)."""
        return self.__geography_id

    @geography_id.setter
    def geography_id(self, value: str):
        self._property_changed('geography_id')
        self.__geography_id = value        

    @property
    def loan_rebate(self) -> float:
        """Rebate paid back to a securities lending borrower."""
        return self.__loan_rebate

    @loan_rebate.setter
    def loan_rebate(self, value: float):
        self._property_changed('loan_rebate')
        self.__loan_rebate = value        

    @property
    def period(self) -> str:
        """Period for the relevant metric, such as 1y (1 year)."""
        return self.__period

    @period.setter
    def period(self, value: str):
        self._property_changed('period')
        self.__period = value        

    @property
    def index_create_source(self) -> str:
        """Source of basket create"""
        return self.__index_create_source

    @index_create_source.setter
    def index_create_source(self, value: str):
        self._property_changed('index_create_source')
        self.__index_create_source = value        

    @property
    def fiscal_quarter(self) -> str:
        """One of the four three-month periods that make up the fiscal year."""
        return self.__fiscal_quarter

    @fiscal_quarter.setter
    def fiscal_quarter(self, value: str):
        self._property_changed('fiscal_quarter')
        self.__fiscal_quarter = value        

    @property
    def version_string(self) -> str:
        """String representing the version number."""
        return self.__version_string

    @version_string.setter
    def version_string(self, value: str):
        self._property_changed('version_string')
        self.__version_string = value        

    @property
    def real_twi_contribution(self) -> float:
        """Contribution of real trade weighted exchange rate index component to real FCI."""
        return self.__real_twi_contribution

    @real_twi_contribution.setter
    def real_twi_contribution(self, value: float):
        self._property_changed('real_twi_contribution')
        self.__real_twi_contribution = value        

    @property
    def market_impact(self) -> float:
        """Market impact is based on the Goldman Sachs Shortfall Model where available
           alongside best estimates from the desk."""
        return self.__market_impact

    @market_impact.setter
    def market_impact(self, value: float):
        self._property_changed('market_impact')
        self.__market_impact = value        

    @property
    def event_type(self) -> str:
        """Equals Analyst Meeting if the event indicates an analyst meeting. Equals
           Earnings Release if the event indicates an earnings release. Equals
           Sales Release when the event indicates a sales release. Indicates
           Drug Data when the event indicates an event related to drugs data.
           Equals Other for any other events."""
        return self.__event_type

    @event_type.setter
    def event_type(self, value: str):
        self._property_changed('event_type')
        self.__event_type = value        

    @property
    def mkt_asset(self) -> str:
        """The MDAPI Asset (e.g. USD, USD/EUR)."""
        return self.__mkt_asset

    @mkt_asset.setter
    def mkt_asset(self, value: str):
        self._property_changed('mkt_asset')
        self.__mkt_asset = value        

    @property
    def asset_count_long(self) -> float:
        """Number of assets in a portfolio with long exposure."""
        return self.__asset_count_long

    @asset_count_long.setter
    def asset_count_long(self, value: float):
        self._property_changed('asset_count_long')
        self.__asset_count_long = value        

    @property
    def spot(self) -> float:
        """Spot price."""
        return self.__spot

    @spot.setter
    def spot(self, value: float):
        self._property_changed('spot')
        self.__spot = value        

    @property
    def last_updated_message(self) -> str:
        """Last Updated Message."""
        return self.__last_updated_message

    @last_updated_message.setter
    def last_updated_message(self, value: str):
        self._property_changed('last_updated_message')
        self.__last_updated_message = value        

    @property
    def underlying_asset_leg2(self) -> str:
        """Same as Underlying Asset 1 if populated."""
        return self.__underlying_asset_leg2

    @underlying_asset_leg2.setter
    def underlying_asset_leg2(self, value: str):
        self._property_changed('underlying_asset_leg2')
        self.__underlying_asset_leg2 = value        

    @property
    def loan_value(self) -> float:
        """The value of the securities or cash delivered by a borrower to a lender to
           support a loan of securities."""
        return self.__loan_value

    @loan_value.setter
    def loan_value(self, value: float):
        self._property_changed('loan_value')
        self.__loan_value = value        

    @property
    def underlying_asset_leg1(self) -> str:
        """The asset, reference asset, or reference obligation for payments of a party???s
           obligations under the SB swap transaction reference."""
        return self.__underlying_asset_leg1

    @underlying_asset_leg1.setter
    def underlying_asset_leg1(self, value: str):
        self._property_changed('underlying_asset_leg1')
        self.__underlying_asset_leg1 = value        

    @property
    def swap_spread(self) -> float:
        """Swap spread."""
        return self.__swap_spread

    @swap_spread.setter
    def swap_spread(self, value: float):
        self._property_changed('swap_spread')
        self.__swap_spread = value        

    @property
    def trading_restriction(self) -> bool:
        """Whether or not the asset has trading restrictions."""
        return self.__trading_restriction

    @trading_restriction.setter
    def trading_restriction(self, value: bool):
        self._property_changed('trading_restriction')
        self.__trading_restriction = value        

    @property
    def asset_parameters_pay_or_receive(self) -> str:
        """Pay or receive fixed"""
        return self.__asset_parameters_pay_or_receive

    @asset_parameters_pay_or_receive.setter
    def asset_parameters_pay_or_receive(self, value: str):
        self._property_changed('asset_parameters_pay_or_receive')
        self.__asset_parameters_pay_or_receive = value        

    @property
    def price_spot_entry_unit(self) -> str:
        """Unit in which the opening price is reported."""
        return self.__price_spot_entry_unit

    @price_spot_entry_unit.setter
    def price_spot_entry_unit(self, value: str):
        self._property_changed('price_spot_entry_unit')
        self.__price_spot_entry_unit = value        

    @property
    def total_return_price(self) -> float:
        """The total return price of an instrument."""
        return self.__total_return_price

    @total_return_price.setter
    def total_return_price(self, value: float):
        self._property_changed('total_return_price')
        self.__total_return_price = value        

    @property
    def weighted_percent_in_model(self) -> float:
        """Weighted percent of constituent in risk model."""
        return self.__weighted_percent_in_model

    @weighted_percent_in_model.setter
    def weighted_percent_in_model(self, value: float):
        self._property_changed('weighted_percent_in_model')
        self.__weighted_percent_in_model = value        

    @property
    def election_period(self) -> str:
        """Period of election."""
        return self.__election_period

    @election_period.setter
    def election_period(self, value: str):
        self._property_changed('election_period')
        self.__election_period = value        

    @property
    def funding_ask_price(self) -> float:
        """Latest Ask Price (price offering to sell)."""
        return self.__funding_ask_price

    @funding_ask_price.setter
    def funding_ask_price(self, value: float):
        self._property_changed('funding_ask_price')
        self.__funding_ask_price = value        

    @property
    def historical_beta(self) -> float:
        """Historical beta."""
        return self.__historical_beta

    @historical_beta.setter
    def historical_beta(self, value: float):
        self._property_changed('historical_beta')
        self.__historical_beta = value        

    @property
    def dissemination_id(self) -> str:
        """DDR generated unique and random ID for reconciliation purpose."""
        return self.__dissemination_id

    @dissemination_id.setter
    def dissemination_id(self, value: str):
        self._property_changed('dissemination_id')
        self.__dissemination_id = value        

    @property
    def bond_risk_premium_index(self) -> float:
        """Bond risk premium index: difference between growth rate forecast and 10y
           treasury yield."""
        return self.__bond_risk_premium_index

    @bond_risk_premium_index.setter
    def bond_risk_premium_index(self, value: float):
        self._property_changed('bond_risk_premium_index')
        self.__bond_risk_premium_index = value        

    @property
    def leg_two_fixed_payment(self) -> float:
        """If fixed payment leg, the fixed payment amount, which is price*number of
           contracts bought*contract unit."""
        return self.__leg_two_fixed_payment

    @leg_two_fixed_payment.setter
    def leg_two_fixed_payment(self, value: float):
        self._property_changed('leg_two_fixed_payment')
        self.__leg_two_fixed_payment = value        

    @property
    def commodity_forecast(self) -> float:
        """Commodity forecast value for the tenor, year or quarter."""
        return self.__commodity_forecast

    @commodity_forecast.setter
    def commodity_forecast(self, value: float):
        self._property_changed('commodity_forecast')
        self.__commodity_forecast = value        

    @property
    def hit_rate_ytd(self) -> float:
        """Hit Rate Ratio Year to Date."""
        return self.__hit_rate_ytd

    @hit_rate_ytd.setter
    def hit_rate_ytd(self, value: float):
        self._property_changed('hit_rate_ytd')
        self.__hit_rate_ytd = value        

    @property
    def valid(self) -> float:
        """Valid."""
        return self.__valid

    @valid.setter
    def valid(self, value: float):
        self._property_changed('valid')
        self.__valid = value        

    @property
    def initial_pricing_date(self) -> datetime.date:
        """Initial pricing date for basket actions."""
        return self.__initial_pricing_date

    @initial_pricing_date.setter
    def initial_pricing_date(self, value: datetime.date):
        self._property_changed('initial_pricing_date')
        self.__initial_pricing_date = value        

    @property
    def indication_of_end_user_exception(self) -> str:
        """If buyer or seller or both is electing the End User Exception."""
        return self.__indication_of_end_user_exception

    @indication_of_end_user_exception.setter
    def indication_of_end_user_exception(self, value: str):
        self._property_changed('indication_of_end_user_exception')
        self.__indication_of_end_user_exception = value        

    @property
    def es_score(self) -> float:
        """E&S numeric score + E&S policy score."""
        return self.__es_score

    @es_score.setter
    def es_score(self, value: float):
        self._property_changed('es_score')
        self.__es_score = value        

    @property
    def price_range_in_ticks(self) -> float:
        """The Price Range of the stock in Ticks on the particular date."""
        return self.__price_range_in_ticks

    @price_range_in_ticks.setter
    def price_range_in_ticks(self, value: float):
        self._property_changed('price_range_in_ticks')
        self.__price_range_in_ticks = value        

    @property
    def expense_ratio_gross_bps(self) -> float:
        """Gives basis point measure of management fee."""
        return self.__expense_ratio_gross_bps

    @expense_ratio_gross_bps.setter
    def expense_ratio_gross_bps(self, value: float):
        self._property_changed('expense_ratio_gross_bps')
        self.__expense_ratio_gross_bps = value        

    @property
    def pct_change(self) -> float:
        """Percentage change of the latest trade price or value from the adjusted
           historical close."""
        return self.__pct_change

    @pct_change.setter
    def pct_change(self, value: float):
        self._property_changed('pct_change')
        self.__pct_change = value        

    @property
    def number_of_rolls(self) -> int:
        """Contract's number of rolls per year."""
        return self.__number_of_rolls

    @number_of_rolls.setter
    def number_of_rolls(self, value: int):
        self._property_changed('number_of_rolls')
        self.__number_of_rolls = value        

    @property
    def agent_lender_fee(self) -> float:
        """Fee earned by the Agent Lender for facilitating a securities lending agreement."""
        return self.__agent_lender_fee

    @agent_lender_fee.setter
    def agent_lender_fee(self, value: float):
        self._property_changed('agent_lender_fee')
        self.__agent_lender_fee = value        

    @property
    def bbid(self) -> str:
        """Bloomberg identifier (ticker and exchange code)."""
        return self.__bbid

    @bbid.setter
    def bbid(self, value: str):
        self._property_changed('bbid')
        self.__bbid = value        

    @property
    def option_strike_price(self) -> float:
        """Strike price of the option. Also called option level."""
        return self.__option_strike_price

    @option_strike_price.setter
    def option_strike_price(self, value: float):
        self._property_changed('option_strike_price')
        self.__option_strike_price = value        

    @property
    def effective_date(self) -> datetime.date:
        """The date at which the measure becomes effective."""
        return self.__effective_date

    @effective_date.setter
    def effective_date(self, value: datetime.date):
        self._property_changed('effective_date')
        self.__effective_date = value        

    @property
    def price_type_leg3(self) -> str:
        """Price denomination and unit of leg 3."""
        return self.__price_type_leg3

    @price_type_leg3.setter
    def price_type_leg3(self, value: str):
        self._property_changed('price_type_leg3')
        self.__price_type_leg3 = value        

    @property
    def arrival_mid_normalized(self) -> float:
        """Performance against Benchmark in pip."""
        return self.__arrival_mid_normalized

    @arrival_mid_normalized.setter
    def arrival_mid_normalized(self, value: float):
        self._property_changed('arrival_mid_normalized')
        self.__arrival_mid_normalized = value        

    @property
    def underlying_asset2(self) -> str:
        """Same as Underlying Asset 1 if populated."""
        return self.__underlying_asset2

    @underlying_asset2.setter
    def underlying_asset2(self, value: str):
        self._property_changed('underlying_asset2')
        self.__underlying_asset2 = value        

    @property
    def underlying_asset1(self) -> str:
        """The asset, reference asset, or reference obligation for payments of a party???s
           obligations under the SB swap transaction reference."""
        return self.__underlying_asset1

    @underlying_asset1.setter
    def underlying_asset1(self, value: str):
        self._property_changed('underlying_asset1')
        self.__underlying_asset1 = value        

    @property
    def rounded_notional_amount_leg1(self) -> float:
        """The total Notional amount or quantity of units of the leg 1 underlying asset."""
        return self.__rounded_notional_amount_leg1

    @rounded_notional_amount_leg1.setter
    def rounded_notional_amount_leg1(self, value: float):
        self._property_changed('rounded_notional_amount_leg1')
        self.__rounded_notional_amount_leg1 = value        

    @property
    def rounded_notional_amount_leg2(self) -> float:
        """The total Notional amount or quantity of units of the leg 2 underlying asset."""
        return self.__rounded_notional_amount_leg2

    @rounded_notional_amount_leg2.setter
    def rounded_notional_amount_leg2(self, value: float):
        self._property_changed('rounded_notional_amount_leg2')
        self.__rounded_notional_amount_leg2 = value        

    @property
    def capped(self) -> str:
        """Whether a trade is capped at the block notional threshold."""
        return self.__capped

    @capped.setter
    def capped(self, value: str):
        self._property_changed('capped')
        self.__capped = value        

    @property
    def rating(self) -> str:
        """Analyst Rating, which may take on the following values."""
        return self.__rating

    @rating.setter
    def rating(self, value: str):
        self._property_changed('rating')
        self.__rating = value        

    @property
    def payment_type_leg1(self) -> str:
        """Type of payment stream on leg 1."""
        return self.__payment_type_leg1

    @payment_type_leg1.setter
    def payment_type_leg1(self, value: str):
        self._property_changed('payment_type_leg1')
        self.__payment_type_leg1 = value        

    @property
    def option_currency(self) -> str:
        """An indication of type of currency on the option premium."""
        return self.__option_currency

    @option_currency.setter
    def option_currency(self, value: str):
        self._property_changed('option_currency')
        self.__option_currency = value        

    @property
    def price_leg3(self) -> float:
        """Price of leg 3."""
        return self.__price_leg3

    @price_leg3.setter
    def price_leg3(self, value: float):
        self._property_changed('price_leg3')
        self.__price_leg3 = value        

    @property
    def price_leg2(self) -> float:
        """Price of leg 2."""
        return self.__price_leg2

    @price_leg2.setter
    def price_leg2(self, value: float):
        self._property_changed('price_leg2')
        self.__price_leg2 = value        

    @property
    def price_leg1(self) -> float:
        """Price of leg 1."""
        return self.__price_leg1

    @price_leg1.setter
    def price_leg1(self, value: float):
        self._property_changed('price_leg1')
        self.__price_leg1 = value        

    @property
    def price_type_leg2(self) -> str:
        """Price denomination and unit of leg 2."""
        return self.__price_type_leg2

    @price_type_leg2.setter
    def price_type_leg2(self, value: str):
        self._property_changed('price_type_leg2')
        self.__price_type_leg2 = value        

    @property
    def legal_entity(self) -> str:
        """Entity that has legal rights to the fund."""
        return self.__legal_entity

    @legal_entity.setter
    def legal_entity(self, value: str):
        self._property_changed('legal_entity')
        self.__legal_entity = value        

    @property
    def performance_fee(self) -> Union[Op, float]:
        return self.__performance_fee

    @performance_fee.setter
    def performance_fee(self, value: Union[Op, float]):
        self._property_changed('performance_fee')
        self.__performance_fee = value        

    @property
    def price_type_leg1(self) -> str:
        """Price denomination and unit of leg 1."""
        return self.__price_type_leg1

    @price_type_leg1.setter
    def price_type_leg1(self, value: str):
        self._property_changed('price_type_leg1')
        self.__price_type_leg1 = value        

    @property
    def payment_type_leg2(self) -> str:
        """Type of payment stream on leg 2."""
        return self.__payment_type_leg2

    @payment_type_leg2.setter
    def payment_type_leg2(self, value: str):
        self._property_changed('payment_type_leg2')
        self.__payment_type_leg2 = value        

    @property
    def type_leg1(self) -> str:
        """Indication if leg 1 is fixed or floating or Physical."""
        return self.__type_leg1

    @type_leg1.setter
    def type_leg1(self, value: str):
        self._property_changed('type_leg1')
        self.__type_leg1 = value        

    @property
    def underlying_asset_ids(self) -> Tuple[str, ...]:
        """Marquee IDs of the underlying assets."""
        return self.__underlying_asset_ids

    @underlying_asset_ids.setter
    def underlying_asset_ids(self, value: Tuple[str, ...]):
        self._property_changed('underlying_asset_ids')
        self.__underlying_asset_ids = value        

    @property
    def type_leg2(self) -> str:
        """Indication if leg 2 is fixed or floating or Physical."""
        return self.__type_leg2

    @type_leg2.setter
    def type_leg2(self, value: str):
        self._property_changed('type_leg2')
        self.__type_leg2 = value        

    @property
    def queue_in_lots_label(self):
        return self.__queue_in_lots_label

    @queue_in_lots_label.setter
    def queue_in_lots_label(self, value):
        self._property_changed('queue_in_lots_label')
        self.__queue_in_lots_label = value        

    @property
    def adv10_day_pct(self) -> float:
        """Median number of shares or units of a given asset traded over a 10 day period."""
        return self.__adv10_day_pct

    @adv10_day_pct.setter
    def adv10_day_pct(self, value: float):
        self._property_changed('adv10_day_pct')
        self.__adv10_day_pct = value        

    @property
    def long_conviction_medium(self) -> float:
        """The count of long ideas with medium conviction."""
        return self.__long_conviction_medium

    @long_conviction_medium.setter
    def long_conviction_medium(self, value: float):
        self._property_changed('long_conviction_medium')
        self.__long_conviction_medium = value        

    @property
    def annual_risk(self) -> float:
        """Annualized risk of a given portfolio, position or asset. Generally computed as
           annualized daily standard deviation of returns."""
        return self.__annual_risk

    @annual_risk.setter
    def annual_risk(self, value: float):
        self._property_changed('annual_risk')
        self.__annual_risk = value        

    @property
    def eti(self) -> str:
        """External Trade Identifier."""
        return self.__eti

    @eti.setter
    def eti(self, value: str):
        self._property_changed('eti')
        self.__eti = value        

    @property
    def daily_tracking_error(self) -> float:
        """Daily tracking error."""
        return self.__daily_tracking_error

    @daily_tracking_error.setter
    def daily_tracking_error(self, value: float):
        self._property_changed('daily_tracking_error')
        self.__daily_tracking_error = value        

    @property
    def leg_two_index(self) -> str:
        """If floating index leg, the index."""
        return self.__leg_two_index

    @leg_two_index.setter
    def leg_two_index(self, value: str):
        self._property_changed('leg_two_index')
        self.__leg_two_index = value        

    @property
    def market_buffer(self) -> float:
        """The actual buffer between holdings and on loan quantity for a market."""
        return self.__market_buffer

    @market_buffer.setter
    def market_buffer(self, value: float):
        self._property_changed('market_buffer')
        self.__market_buffer = value        

    @property
    def market_cap(self) -> float:
        """Market capitalization of a given asset in denominated currency."""
        return self.__market_cap

    @market_cap.setter
    def market_cap(self, value: float):
        self._property_changed('market_cap')
        self.__market_cap = value        

    @property
    def oe_id(self) -> str:
        """Marquee unique identifier"""
        return self.__oe_id

    @oe_id.setter
    def oe_id(self, value: str):
        self._property_changed('oe_id')
        self.__oe_id = value        

    @property
    def cluster_region(self):
        return self.__cluster_region

    @cluster_region.setter
    def cluster_region(self, value):
        self._property_changed('cluster_region')
        self.__cluster_region = value        

    @property
    def bbid_equivalent(self) -> str:
        """Bloomberg identifier (ticker and country code) equivalent - i.e. for OTCs
           options, the equivalent BBID on exchange."""
        return self.__bbid_equivalent

    @bbid_equivalent.setter
    def bbid_equivalent(self, value: str):
        self._property_changed('bbid_equivalent')
        self.__bbid_equivalent = value        

    @property
    def valoren(self) -> str:
        """Valoren or VALOR number, Swiss primary security identifier (subject to
           licensing)."""
        return self.__valoren

    @valoren.setter
    def valoren(self, value: str):
        self._property_changed('valoren')
        self.__valoren = value        

    @property
    def basis(self) -> float:
        """Spread to be added to the shorter tenor leg for the swap to be ATM."""
        return self.__basis

    @basis.setter
    def basis(self, value: float):
        self._property_changed('basis')
        self.__basis = value        

    @property
    def investment_rate_trend(self) -> float:
        """The day over day trend of the rate of return on an investment."""
        return self.__investment_rate_trend

    @investment_rate_trend.setter
    def investment_rate_trend(self, value: float):
        self._property_changed('investment_rate_trend')
        self.__investment_rate_trend = value        

    @property
    def ext_mkt_class(self) -> str:
        """External MDAPI class."""
        return self.__ext_mkt_class

    @ext_mkt_class.setter
    def ext_mkt_class(self, value: str):
        self._property_changed('ext_mkt_class')
        self.__ext_mkt_class = value        

    @property
    def price_currency(self) -> str:
        """Denominated pricing currency."""
        return self.__price_currency

    @price_currency.setter
    def price_currency(self, value: str):
        self._property_changed('price_currency')
        self.__price_currency = value        

    @property
    def hedge_id(self) -> str:
        """Marquee unique identifier for a hedge."""
        return self.__hedge_id

    @hedge_id.setter
    def hedge_id(self, value: str):
        self._property_changed('hedge_id')
        self.__hedge_id = value        

    @property
    def tcm_cost_horizon8_day(self) -> float:
        """TCM cost with a 8 day time horizon."""
        return self.__tcm_cost_horizon8_day

    @tcm_cost_horizon8_day.setter
    def tcm_cost_horizon8_day(self, value: float):
        self._property_changed('tcm_cost_horizon8_day')
        self.__tcm_cost_horizon8_day = value        

    @property
    def residual_variance(self) -> float:
        """Residual variance."""
        return self.__residual_variance

    @residual_variance.setter
    def residual_variance(self, value: float):
        self._property_changed('residual_variance')
        self.__residual_variance = value        

    @property
    def supra_strategy(self) -> str:
        """Broad descriptor of a fund's investment approach. Same view permissions as the
           asset"""
        return self.__supra_strategy

    @supra_strategy.setter
    def supra_strategy(self, value: str):
        self._property_changed('supra_strategy')
        self.__supra_strategy = value        

    @property
    def restrict_internal_derived_data(self) -> bool:
        """Restricts Ability to Use Internally as Part of Derived Data."""
        return self.__restrict_internal_derived_data

    @restrict_internal_derived_data.setter
    def restrict_internal_derived_data(self, value: bool):
        self._property_changed('restrict_internal_derived_data')
        self.__restrict_internal_derived_data = value        

    @property
    def day_count_convention(self) -> str:
        """The determination of how interest accrues over time for the SB swap."""
        return self.__day_count_convention

    @day_count_convention.setter
    def day_count_convention(self, value: str):
        self._property_changed('day_count_convention')
        self.__day_count_convention = value        

    @property
    def rounded_notional_amount1(self) -> float:
        """The total Notional amount or quantity of units of the underlying asset."""
        return self.__rounded_notional_amount1

    @rounded_notional_amount1.setter
    def rounded_notional_amount1(self, value: float):
        self._property_changed('rounded_notional_amount1')
        self.__rounded_notional_amount1 = value        

    @property
    def adv5_day_pct(self) -> float:
        """Median number of shares or units of a given asset traded over a 5 day period."""
        return self.__adv5_day_pct

    @adv5_day_pct.setter
    def adv5_day_pct(self, value: float):
        self._property_changed('adv5_day_pct')
        self.__adv5_day_pct = value        

    @property
    def rounded_notional_amount2(self) -> float:
        """Same as Rounded Notional Amount 1."""
        return self.__rounded_notional_amount2

    @rounded_notional_amount2.setter
    def rounded_notional_amount2(self, value: float):
        self._property_changed('rounded_notional_amount2')
        self.__rounded_notional_amount2 = value        

    @property
    def lending_sec_type(self) -> str:
        """Securities lending identifiter for the security on loan."""
        return self.__lending_sec_type

    @lending_sec_type.setter
    def lending_sec_type(self, value: str):
        self._property_changed('lending_sec_type')
        self.__lending_sec_type = value        

    @property
    def leverage(self) -> float:
        """Leverage."""
        return self.__leverage

    @leverage.setter
    def leverage(self, value: float):
        self._property_changed('leverage')
        self.__leverage = value        

    @property
    def option_family(self) -> str:
        """Style of the option."""
        return self.__option_family

    @option_family.setter
    def option_family(self, value: str):
        self._property_changed('option_family')
        self.__option_family = value        

    @property
    def price_spot_stop_loss_value(self) -> float:
        """Stop loss price value of the trade idea."""
        return self.__price_spot_stop_loss_value

    @price_spot_stop_loss_value.setter
    def price_spot_stop_loss_value(self, value: float):
        self._property_changed('price_spot_stop_loss_value')
        self.__price_spot_stop_loss_value = value        

    @property
    def kpi_id(self) -> str:
        """Marquee unique KPI identifier."""
        return self.__kpi_id

    @kpi_id.setter
    def kpi_id(self, value: str):
        self._property_changed('kpi_id')
        self.__kpi_id = value        

    @property
    def relative_return_wtd(self) -> float:
        """Relative Return Week to Date."""
        return self.__relative_return_wtd

    @relative_return_wtd.setter
    def relative_return_wtd(self, value: float):
        self._property_changed('relative_return_wtd')
        self.__relative_return_wtd = value        

    @property
    def borrow_cost(self) -> float:
        """An indication of the rate one would be charged for borrowing/shorting the
           relevant asset on that day, expressed in bps. Rates may change daily."""
        return self.__borrow_cost

    @borrow_cost.setter
    def borrow_cost(self, value: float):
        self._property_changed('borrow_cost')
        self.__borrow_cost = value        

    @property
    def average_implied_volatility(self) -> float:
        """Average volatility of an asset implied by observations of market prices."""
        return self.__average_implied_volatility

    @average_implied_volatility.setter
    def average_implied_volatility(self, value: float):
        self._property_changed('average_implied_volatility')
        self.__average_implied_volatility = value        

    @property
    def fair_value(self) -> float:
        """Fair Value."""
        return self.__fair_value

    @fair_value.setter
    def fair_value(self, value: float):
        self._property_changed('fair_value')
        self.__fair_value = value        

    @property
    def adjusted_high_price(self) -> float:
        """Adjusted high level of an asset based on official exchange fixing or calculation
           agent marked level."""
        return self.__adjusted_high_price

    @adjusted_high_price.setter
    def adjusted_high_price(self, value: float):
        self._property_changed('adjusted_high_price')
        self.__adjusted_high_price = value        

    @property
    def open_time(self) -> datetime.datetime:
        """Time opened. ISO 8601 formatted string."""
        return self.__open_time

    @open_time.setter
    def open_time(self, value: datetime.datetime):
        self._property_changed('open_time')
        self.__open_time = value        

    @property
    def local_ccy_rate(self) -> float:
        """The interest rate of the local currency of the associated FX contract."""
        return self.__local_ccy_rate

    @local_ccy_rate.setter
    def local_ccy_rate(self, value: float):
        self._property_changed('local_ccy_rate')
        self.__local_ccy_rate = value        

    @property
    def ext_mkt_point1(self) -> str:
        """First dimension of external MDAPI point."""
        return self.__ext_mkt_point1

    @ext_mkt_point1.setter
    def ext_mkt_point1(self, value: str):
        self._property_changed('ext_mkt_point1')
        self.__ext_mkt_point1 = value        

    @property
    def direction(self) -> str:
        """Indicates whether exposure of a given position is long or short."""
        return self.__direction

    @direction.setter
    def direction(self, value: str):
        self._property_changed('direction')
        self.__direction = value        

    @property
    def ext_mkt_point2(self) -> str:
        """Second dimension of external MDAPI point."""
        return self.__ext_mkt_point2

    @ext_mkt_point2.setter
    def ext_mkt_point2(self, value: str):
        self._property_changed('ext_mkt_point2')
        self.__ext_mkt_point2 = value        

    @property
    def sub_region_code(self) -> str:
        """ISO 3166 Sub Region Code."""
        return self.__sub_region_code

    @sub_region_code.setter
    def sub_region_code(self, value: str):
        self._property_changed('sub_region_code')
        self.__sub_region_code = value        

    @property
    def value_forecast(self) -> str:
        """Average forecast among a representative group of economists."""
        return self.__value_forecast

    @value_forecast.setter
    def value_forecast(self, value: str):
        self._property_changed('value_forecast')
        self.__value_forecast = value        

    @property
    def execution_venue(self) -> str:
        """An indication of whether the SB swap transaction was executed on a registered
           swap execution facility or designated contract market or was executed
           as an off-facility swap."""
        return self.__execution_venue

    @execution_venue.setter
    def execution_venue(self, value: str):
        self._property_changed('execution_venue')
        self.__execution_venue = value        

    @property
    def position_source_type(self) -> str:
        """Source object for position data"""
        return self.__position_source_type

    @position_source_type.setter
    def position_source_type(self, value: str):
        self._property_changed('position_source_type')
        self.__position_source_type = value        

    @property
    def approve_rebalance(self) -> bool:
        """An approved basket."""
        return self.__approve_rebalance

    @approve_rebalance.setter
    def approve_rebalance(self, value: bool):
        self._property_changed('approve_rebalance')
        self.__approve_rebalance = value        

    @property
    def adjusted_close_price(self) -> float:
        """Closing Price adjusted for corporate actions."""
        return self.__adjusted_close_price

    @adjusted_close_price.setter
    def adjusted_close_price(self, value: float):
        self._property_changed('adjusted_close_price')
        self.__adjusted_close_price = value        

    @property
    def lms_id(self) -> str:
        """Market identifier code."""
        return self.__lms_id

    @lms_id.setter
    def lms_id(self, value: str):
        self._property_changed('lms_id')
        self.__lms_id = value        

    @property
    def rebate_rate(self) -> float:
        """Defines the rate of the cash-back payment to an investor who puts up collateral
           in borrowing a stock. A rebate rate of interest implies a fee for the
           loan of securities."""
        return self.__rebate_rate

    @rebate_rate.setter
    def rebate_rate(self, value: float):
        self._property_changed('rebate_rate')
        self.__rebate_rate = value        

    @property
    def participation_rate(self) -> float:
        """Executed quantity over market volume (e.g. 5, 10, 20)."""
        return self.__participation_rate

    @participation_rate.setter
    def participation_rate(self, value: float):
        self._property_changed('participation_rate')
        self.__participation_rate = value        

    @property
    def obfr(self) -> float:
        """The overnight bank funding rate."""
        return self.__obfr

    @obfr.setter
    def obfr(self, value: float):
        self._property_changed('obfr')
        self.__obfr = value        

    @property
    def option_lock_period(self) -> str:
        """An indication of the first allowable exercise date of the option."""
        return self.__option_lock_period

    @option_lock_period.setter
    def option_lock_period(self, value: str):
        self._property_changed('option_lock_period')
        self.__option_lock_period = value        

    @property
    def strike_relative(self) -> Union[float, str]:
        """Strike as value, percent or at-the-money e.g. 62.5, 95%, ATM-25, ATMF"""
        return self.__strike_relative

    @strike_relative.setter
    def strike_relative(self, value: Union[float, str]):
        self._property_changed('strike_relative')
        self.__strike_relative = value        

    @property
    def es_momentum_percentile(self) -> float:
        """A percentile that captures a company???s E&S momentum ranking within its
           subsector."""
        return self.__es_momentum_percentile

    @es_momentum_percentile.setter
    def es_momentum_percentile(self, value: float):
        self._property_changed('es_momentum_percentile')
        self.__es_momentum_percentile = value        

    @property
    def price_notation(self) -> float:
        """The Basis points, Price, Yield, Spread, Coupon, etc., value depending on the
           type of SB swap, which is calculated at affirmation."""
        return self.__price_notation

    @price_notation.setter
    def price_notation(self, value: float):
        self._property_changed('price_notation')
        self.__price_notation = value        

    @property
    def strategy(self) -> str:
        """More specific descriptor of a fund's investment approach. Same view permissions
           as the asset."""
        return self.__strategy

    @strategy.setter
    def strategy(self, value: str):
        self._property_changed('strategy')
        self.__strategy = value        

    @property
    def forecast_date(self) -> datetime.date:
        """Date of forecasted electricity loads."""
        return self.__forecast_date

    @forecast_date.setter
    def forecast_date(self, value: datetime.date):
        self._property_changed('forecast_date')
        self.__forecast_date = value        

    @property
    def position_type(self) -> str:
        """Type of positions."""
        return self.__position_type

    @position_type.setter
    def position_type(self, value: str):
        self._property_changed('position_type')
        self.__position_type = value        

    @property
    def lender_income(self) -> float:
        """Income earned by the Lender for the loan of securities to a borrower."""
        return self.__lender_income

    @lender_income.setter
    def lender_income(self, value: float):
        self._property_changed('lender_income')
        self.__lender_income = value        

    @property
    def sub_asset_class(self) -> str:
        """An indication of the sub asset class."""
        return self.__sub_asset_class

    @sub_asset_class.setter
    def sub_asset_class(self, value: str):
        self._property_changed('sub_asset_class')
        self.__sub_asset_class = value        

    @property
    def provide_mpl_tape_b(self) -> float:
        """Goldman's rate for midpoint pegged liquidity providing trades on tape B."""
        return self.__provide_mpl_tape_b

    @provide_mpl_tape_b.setter
    def provide_mpl_tape_b(self, value: float):
        self._property_changed('provide_mpl_tape_b')
        self.__provide_mpl_tape_b = value        

    @property
    def short_interest(self) -> float:
        """Short interest value."""
        return self.__short_interest

    @short_interest.setter
    def short_interest(self, value: float):
        self._property_changed('short_interest')
        self.__short_interest = value        

    @property
    def reference_period(self) -> str:
        """The period for which released data refers to."""
        return self.__reference_period

    @reference_period.setter
    def reference_period(self, value: str):
        self._property_changed('reference_period')
        self.__reference_period = value        

    @property
    def provide_mpl_tape_c(self) -> float:
        """Goldman's rate for midpoint pegged liquidity providing trades on tape C."""
        return self.__provide_mpl_tape_c

    @provide_mpl_tape_c.setter
    def provide_mpl_tape_c(self, value: float):
        self._property_changed('provide_mpl_tape_c')
        self.__provide_mpl_tape_c = value        

    @property
    def adjusted_volume(self) -> float:
        """Accumulated number of shares, lots or contracts traded according to the market
           convention adjusted for corporate actions."""
        return self.__adjusted_volume

    @adjusted_volume.setter
    def adjusted_volume(self, value: float):
        self._property_changed('adjusted_volume')
        self.__adjusted_volume = value        

    @property
    def provide_mpl_tape_a(self) -> float:
        """Goldman's rate for midpoint pegged liquidity providing trades on tape A."""
        return self.__provide_mpl_tape_a

    @provide_mpl_tape_a.setter
    def provide_mpl_tape_a(self, value: float):
        self._property_changed('provide_mpl_tape_a')
        self.__provide_mpl_tape_a = value        

    @property
    def owner_id(self) -> str:
        """Marquee unique identifier for user who owns the object."""
        return self.__owner_id

    @owner_id.setter
    def owner_id(self, value: str):
        self._property_changed('owner_id')
        self.__owner_id = value        

    @property
    def composite10_day_adv(self) -> float:
        """Composite 10 day ADV."""
        return self.__composite10_day_adv

    @composite10_day_adv.setter
    def composite10_day_adv(self, value: float):
        self._property_changed('composite10_day_adv')
        self.__composite10_day_adv = value        

    @property
    def bpe_quality_stars(self) -> float:
        """Confidence in the BPE."""
        return self.__bpe_quality_stars

    @bpe_quality_stars.setter
    def bpe_quality_stars(self, value: float):
        self._property_changed('bpe_quality_stars')
        self.__bpe_quality_stars = value        

    @property
    def idea_activity_type(self) -> str:
        """Equals CorporateAction if the activity originates as a result of a corporate
           action. Equals GovernanceAction if the activity originates as a
           result of a control measure. Equals UserAction if the activity is
           user driven."""
        return self.__idea_activity_type

    @idea_activity_type.setter
    def idea_activity_type(self, value: str):
        self._property_changed('idea_activity_type')
        self.__idea_activity_type = value        

    @property
    def idea_source(self) -> str:
        """Equals User if the idea activity originates from a sales person. Equals System
           if the idea activity is system generated."""
        return self.__idea_source

    @idea_source.setter
    def idea_source(self, value: str):
        self._property_changed('idea_source')
        self.__idea_source = value        

    @property
    def unadjusted_ask(self) -> float:
        """Unadjusted ask level of an asset based on official exchange fixing or
           calculation agent marked level."""
        return self.__unadjusted_ask

    @unadjusted_ask.setter
    def unadjusted_ask(self, value: float):
        self._property_changed('unadjusted_ask')
        self.__unadjusted_ask = value        

    @property
    def trading_pnl(self) -> float:
        """Trading Profit and Loss (PNL)."""
        return self.__trading_pnl

    @trading_pnl.setter
    def trading_pnl(self, value: float):
        self._property_changed('trading_pnl')
        self.__trading_pnl = value        

    @property
    def collateral_value_required(self) -> float:
        """Value of collateral required to cover a given position."""
        return self.__collateral_value_required

    @collateral_value_required.setter
    def collateral_value_required(self, value: float):
        self._property_changed('collateral_value_required')
        self.__collateral_value_required = value        

    @property
    def given_plus_paid(self) -> float:
        """Total of given & paid."""
        return self.__given_plus_paid

    @given_plus_paid.setter
    def given_plus_paid(self, value: float):
        self._property_changed('given_plus_paid')
        self.__given_plus_paid = value        

    @property
    def short_conviction_small(self) -> float:
        """The count of short ideas with small conviction."""
        return self.__short_conviction_small

    @short_conviction_small.setter
    def short_conviction_small(self, value: float):
        self._property_changed('short_conviction_small')
        self.__short_conviction_small = value        

    @property
    def price_to_earnings_positive(self) -> float:
        """Price to earnings positive."""
        return self.__price_to_earnings_positive

    @price_to_earnings_positive.setter
    def price_to_earnings_positive(self, value: float):
        self._property_changed('price_to_earnings_positive')
        self.__price_to_earnings_positive = value        

    @property
    def forecast(self) -> float:
        """Forward FX forecast."""
        return self.__forecast

    @forecast.setter
    def forecast(self, value: float):
        self._property_changed('forecast')
        self.__forecast = value        

    @property
    def pnl(self) -> float:
        """Profit and Loss."""
        return self.__pnl

    @pnl.setter
    def pnl(self, value: float):
        self._property_changed('pnl')
        self.__pnl = value        

    @property
    def upfront_payment_currency(self) -> str:
        """Currency of upfront payment."""
        return self.__upfront_payment_currency

    @upfront_payment_currency.setter
    def upfront_payment_currency(self, value: str):
        self._property_changed('upfront_payment_currency')
        self.__upfront_payment_currency = value        

    @property
    def date_index(self) -> float:
        """For a rates asset, represents the proxy for a meeting number."""
        return self.__date_index

    @date_index.setter
    def date_index(self, value: float):
        self._property_changed('date_index')
        self.__date_index = value        

    @property
    def tcm_cost_horizon4_day(self) -> float:
        """TCM cost with a 4 day time horizon."""
        return self.__tcm_cost_horizon4_day

    @tcm_cost_horizon4_day.setter
    def tcm_cost_horizon4_day(self, value: float):
        self._property_changed('tcm_cost_horizon4_day')
        self.__tcm_cost_horizon4_day = value        

    @property
    def asset_classifications_is_primary(self) -> bool:
        """Whether or not it is the primary exchange asset."""
        return self.__asset_classifications_is_primary

    @asset_classifications_is_primary.setter
    def asset_classifications_is_primary(self, value: bool):
        self._property_changed('asset_classifications_is_primary')
        self.__asset_classifications_is_primary = value        

    @property
    def styles(self) -> Tuple[Tuple[str, ...], ...]:
        """Styles or themes associated with the asset (max 50)"""
        return self.__styles

    @styles.setter
    def styles(self, value: Tuple[Tuple[str, ...], ...]):
        self._property_changed('styles')
        self.__styles = value        

    @property
    def short_name(self) -> str:
        """Short name."""
        return self.__short_name

    @short_name.setter
    def short_name(self, value: str):
        self._property_changed('short_name')
        self.__short_name = value        

    @property
    def dwi_contribution(self) -> float:
        """Contribution of debt weighted exchange rate index to FCI. Only applicable to EM
           countries."""
        return self.__dwi_contribution

    @dwi_contribution.setter
    def dwi_contribution(self, value: float):
        self._property_changed('dwi_contribution')
        self.__dwi_contribution = value        

    @property
    def reset_frequency1(self) -> str:
        """An integer multiplier of a period describing how often the parties to an SB swap
           transaction shall evaluate and, when applicable, change the price
           used for the underlying assets of the swap transaction. Such reset
           frequency may be described as one letter preceded by an integer."""
        return self.__reset_frequency1

    @reset_frequency1.setter
    def reset_frequency1(self, value: str):
        self._property_changed('reset_frequency1')
        self.__reset_frequency1 = value        

    @property
    def asset2_id(self) -> str:
        """Marquee unique asset identifier."""
        return self.__asset2_id

    @asset2_id.setter
    def asset2_id(self, value: str):
        self._property_changed('asset2_id')
        self.__asset2_id = value        

    @property
    def reset_frequency2(self) -> str:
        """Same as Reset Frequency 1."""
        return self.__reset_frequency2

    @reset_frequency2.setter
    def reset_frequency2(self, value: str):
        self._property_changed('reset_frequency2')
        self.__reset_frequency2 = value        

    @property
    def average_fill_price(self) -> float:
        """Average fill price for the order since it started."""
        return self.__average_fill_price

    @average_fill_price.setter
    def average_fill_price(self, value: float):
        self._property_changed('average_fill_price')
        self.__average_fill_price = value        

    @property
    def price_notation_type2(self) -> str:
        """Basis points, Price, Yield, Spread, Coupon, etc., depending on the type of SB
           swap, which is calculated at affirmation."""
        return self.__price_notation_type2

    @price_notation_type2.setter
    def price_notation_type2(self, value: str):
        self._property_changed('price_notation_type2')
        self.__price_notation_type2 = value        

    @property
    def price_notation_type3(self) -> str:
        """Basis points, Price, Yield, Spread, Coupon, etc., depending on the type of SB
           swap, which is calculated at affirmation."""
        return self.__price_notation_type3

    @price_notation_type3.setter
    def price_notation_type3(self, value: str):
        self._property_changed('price_notation_type3')
        self.__price_notation_type3 = value        

    @property
    def bid_gspread(self) -> float:
        """Bid G spread."""
        return self.__bid_gspread

    @bid_gspread.setter
    def bid_gspread(self, value: float):
        self._property_changed('bid_gspread')
        self.__bid_gspread = value        

    @property
    def open_price(self) -> float:
        """Opening level of an asset based on official exchange fixing or calculation agent
           marked level."""
        return self.__open_price

    @open_price.setter
    def open_price(self, value: float):
        self._property_changed('open_price')
        self.__open_price = value        

    @property
    def depth_spread_score(self) -> float:
        """Z-score of the difference between the mid price and the best price an order to
           buy or sell a specific notional can be filled at."""
        return self.__depth_spread_score

    @depth_spread_score.setter
    def depth_spread_score(self, value: float):
        self._property_changed('depth_spread_score')
        self.__depth_spread_score = value        

    @property
    def sub_account(self) -> str:
        """Subaccount."""
        return self.__sub_account

    @sub_account.setter
    def sub_account(self, value: str):
        self._property_changed('sub_account')
        self.__sub_account = value        

    @property
    def notional_currency_leg1(self) -> str:
        """An indication of the type of currency of the notional or principal amount on leg
           1."""
        return self.__notional_currency_leg1

    @notional_currency_leg1.setter
    def notional_currency_leg1(self, value: str):
        self._property_changed('notional_currency_leg1')
        self.__notional_currency_leg1 = value        

    @property
    def notional_currency_leg2(self) -> str:
        """An indication of the type of currency of the notional or principal amount on leg
           2."""
        return self.__notional_currency_leg2

    @notional_currency_leg2.setter
    def notional_currency_leg2(self, value: str):
        self._property_changed('notional_currency_leg2')
        self.__notional_currency_leg2 = value        

    @property
    def fair_volatility(self) -> float:
        """Strike in volatility terms, calculated as square root of fair variance."""
        return self.__fair_volatility

    @fair_volatility.setter
    def fair_volatility(self, value: float):
        self._property_changed('fair_volatility')
        self.__fair_volatility = value        

    @property
    def portfolio_type(self) -> str:
        """Portfolio type differentiates the portfolio categorization"""
        return self.__portfolio_type

    @portfolio_type.setter
    def portfolio_type(self, value: str):
        self._property_changed('portfolio_type')
        self.__portfolio_type = value        

    @property
    def vendor(self) -> Union[Union[MarketDataVendor, str], Union[RiskModelVendor, str]]:
        return self.__vendor

    @vendor.setter
    def vendor(self, value: Union[Union[MarketDataVendor, str], Union[RiskModelVendor, str]]):
        self._property_changed('vendor')
        self.__vendor = value        

    @property
    def currency(self) -> str:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: str):
        self._property_changed('currency')
        self.__currency = value        

    @property
    def cluster_class(self) -> str:
        """The Cluster the stock belongs to on the particular date. The cluster class will
           be assigned to a value between 1 and 13 (inclusive)."""
        return self.__cluster_class

    @cluster_class.setter
    def cluster_class(self, value: str):
        self._property_changed('cluster_class')
        self.__cluster_class = value        

    @property
    def queueing_time(self) -> int:
        """Time for which risk calculation was queued (ms)."""
        return self.__queueing_time

    @queueing_time.setter
    def queueing_time(self, value: int):
        self._property_changed('queueing_time')
        self.__queueing_time = value        

    @property
    def ann_return5_year(self) -> float:
        """Total return representing past performance, used for GS Money Market onshore
           funds, over five years."""
        return self.__ann_return5_year

    @ann_return5_year.setter
    def ann_return5_year(self, value: float):
        self._property_changed('ann_return5_year')
        self.__ann_return5_year = value        

    @property
    def bid_size(self) -> float:
        """The number of shares, lots, or contracts willing to buy at the Bid price."""
        return self.__bid_size

    @bid_size.setter
    def bid_size(self, value: float):
        self._property_changed('bid_size')
        self.__bid_size = value        

    @property
    def arrival_mid(self) -> float:
        """Arrival Mid Price."""
        return self.__arrival_mid

    @arrival_mid.setter
    def arrival_mid(self, value: float):
        self._property_changed('arrival_mid')
        self.__arrival_mid = value        

    @property
    def business_sponsor(self) -> str:
        """Business Sponsor."""
        return self.__business_sponsor

    @business_sponsor.setter
    def business_sponsor(self, value: str):
        self._property_changed('business_sponsor')
        self.__business_sponsor = value        

    @property
    def asset_parameters_exchange_currency(self) -> str:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__asset_parameters_exchange_currency

    @asset_parameters_exchange_currency.setter
    def asset_parameters_exchange_currency(self, value: str):
        self._property_changed('asset_parameters_exchange_currency')
        self.__asset_parameters_exchange_currency = value        

    @property
    def unexplained(self) -> float:
        """PNL unexplained by risk model."""
        return self.__unexplained

    @unexplained.setter
    def unexplained(self, value: float):
        self._property_changed('unexplained')
        self.__unexplained = value        

    @property
    def candidate_name(self) -> str:
        """Name of candidate in election."""
        return self.__candidate_name

    @candidate_name.setter
    def candidate_name(self, value: str):
        self._property_changed('candidate_name')
        self.__candidate_name = value        

    @property
    def metric(self) -> str:
        """Metric for the associated asset."""
        return self.__metric

    @metric.setter
    def metric(self, value: str):
        self._property_changed('metric')
        self.__metric = value        

    @property
    def ask(self) -> float:
        """Latest Ask Price (price offering to sell)."""
        return self.__ask

    @ask.setter
    def ask(self, value: float):
        self._property_changed('ask')
        self.__ask = value        

    @property
    def close_price(self) -> float:
        """Closing level of an asset based on official exchange fixing or calculation agent
           marked level."""
        return self.__close_price

    @close_price.setter
    def close_price(self, value: float):
        self._property_changed('close_price')
        self.__close_price = value        

    @property
    def end_time(self) -> datetime.datetime:
        """End time."""
        return self.__end_time

    @end_time.setter
    def end_time(self, value: datetime.datetime):
        self._property_changed('end_time')
        self.__end_time = value        

    @property
    def execution_timestamp(self) -> datetime.datetime:
        """The time and date of execution of the publicly reportable swap transaction in
           Coordinated Universal Time (UTC - CCYY-MMDDThh:mm:ss)."""
        return self.__execution_timestamp

    @execution_timestamp.setter
    def execution_timestamp(self, value: datetime.datetime):
        self._property_changed('execution_timestamp')
        self.__execution_timestamp = value        

    @property
    def source(self) -> str:
        """Source of data."""
        return self.__source

    @source.setter
    def source(self, value: str):
        self._property_changed('source')
        self.__source = value        

    @property
    def expense_ratio_net_bps(self) -> float:
        """Gives basis point measure of management fee, net."""
        return self.__expense_ratio_net_bps

    @expense_ratio_net_bps.setter
    def expense_ratio_net_bps(self, value: float):
        self._property_changed('expense_ratio_net_bps')
        self.__expense_ratio_net_bps = value        

    @property
    def data_set_sub_category(self) -> str:
        """Second level grouping of dataset."""
        return self.__data_set_sub_category

    @data_set_sub_category.setter
    def data_set_sub_category(self, value: str):
        self._property_changed('data_set_sub_category')
        self.__data_set_sub_category = value        

    @property
    def day_count_convention2(self) -> str:
        """Day count convention for leg 2."""
        return self.__day_count_convention2

    @day_count_convention2.setter
    def day_count_convention2(self, value: str):
        self._property_changed('day_count_convention2')
        self.__day_count_convention2 = value        

    @property
    def quantity_bucket(self) -> str:
        """Range of pricing hours."""
        return self.__quantity_bucket

    @quantity_bucket.setter
    def quantity_bucket(self, value: str):
        self._property_changed('quantity_bucket')
        self.__quantity_bucket = value        

    @property
    def factor_two(self) -> str:
        """For Axioma, one of: Exchange Rate Sensitivity, Growth, Leverage, Medium-Term
           Momentum, Short-Term Momentum, Size, Value, Volatility. For Prime,
           one of: Long Concentration, Short Concentration, Long Crowdedness,
           Short Crowdedness, Crowdedness momentum, Short Conviction."""
        return self.__factor_two

    @factor_two.setter
    def factor_two(self, value: str):
        self._property_changed('factor_two')
        self.__factor_two = value        

    @property
    def oe_name(self) -> str:
        """Name of user's organization."""
        return self.__oe_name

    @oe_name.setter
    def oe_name(self, value: str):
        self._property_changed('oe_name')
        self.__oe_name = value        

    @property
    def given(self) -> float:
        """Number of trades given."""
        return self.__given

    @given.setter
    def given(self, value: float):
        self._property_changed('given')
        self.__given = value        

    @property
    def delisting_date(self) -> str:
        """Date at which the entity is delisted."""
        return self.__delisting_date

    @delisting_date.setter
    def delisting_date(self, value: str):
        self._property_changed('delisting_date')
        self.__delisting_date = value        

    @property
    def price_spot_target_value(self) -> float:
        """Target price value of the trade idea."""
        return self.__price_spot_target_value

    @price_spot_target_value.setter
    def price_spot_target_value(self, value: float):
        self._property_changed('price_spot_target_value')
        self.__price_spot_target_value = value        

    @property
    def weight(self) -> float:
        """Weight of a given position within a portfolio, by default calcualted as
           netWeight."""
        return self.__weight

    @weight.setter
    def weight(self, value: float):
        self._property_changed('weight')
        self.__weight = value        

    @property
    def business_scope(self) -> str:
        """Business/Product Scope."""
        return self.__business_scope

    @business_scope.setter
    def business_scope(self, value: str):
        self._property_changed('business_scope')
        self.__business_scope = value        

    @property
    def market_data_point(self) -> Tuple[Tuple[str, ...], ...]:
        """The market data point (e.g. 3m, 10y, 11y, Dec19)."""
        return self.__market_data_point

    @market_data_point.setter
    def market_data_point(self, value: Tuple[Tuple[str, ...], ...]):
        self._property_changed('market_data_point')
        self.__market_data_point = value        

    @property
    def absolute_weight(self) -> float:
        """Weight in terms of absolute notional."""
        return self.__absolute_weight

    @absolute_weight.setter
    def absolute_weight(self, value: float):
        self._property_changed('absolute_weight')
        self.__absolute_weight = value        

    @property
    def trade_time(self) -> datetime.datetime:
        """Trade Time."""
        return self.__trade_time

    @trade_time.setter
    def trade_time(self, value: datetime.datetime):
        self._property_changed('trade_time')
        self.__trade_time = value        

    @property
    def measure(self) -> str:
        """A calculated metric in the risk scenario."""
        return self.__measure

    @measure.setter
    def measure(self, value: str):
        self._property_changed('measure')
        self.__measure = value        

    @property
    def hedge_annualized_volatility(self) -> float:
        """Standard deviation of the annualized returns."""
        return self.__hedge_annualized_volatility

    @hedge_annualized_volatility.setter
    def hedge_annualized_volatility(self, value: float):
        self._property_changed('hedge_annualized_volatility')
        self.__hedge_annualized_volatility = value        

    @property
    def benchmark_currency(self) -> str:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__benchmark_currency

    @benchmark_currency.setter
    def benchmark_currency(self, value: str):
        self._property_changed('benchmark_currency')
        self.__benchmark_currency = value        

    @property
    def futures_contract(self) -> str:
        """The related futures contract code if applicable."""
        return self.__futures_contract

    @futures_contract.setter
    def futures_contract(self, value: str):
        self._property_changed('futures_contract')
        self.__futures_contract = value        

    @property
    def name(self) -> str:
        """Legal or published name for the asset."""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def aum(self) -> Union[Op, float]:
        return self.__aum

    @aum.setter
    def aum(self, value: Union[Op, float]):
        self._property_changed('aum')
        self.__aum = value        

    @property
    def folder_name(self) -> str:
        """Folder Name of a chart."""
        return self.__folder_name

    @folder_name.setter
    def folder_name(self, value: str):
        self._property_changed('folder_name')
        self.__folder_name = value        

    @property
    def option_expiration_date(self) -> datetime.date:
        """An indication of the date that the option is no longer available for exercise."""
        return self.__option_expiration_date

    @option_expiration_date.setter
    def option_expiration_date(self, value: datetime.date):
        self._property_changed('option_expiration_date')
        self.__option_expiration_date = value        

    @property
    def swaption_atm_fwd_rate(self) -> float:
        """Swaption ATM forward rate."""
        return self.__swaption_atm_fwd_rate

    @swaption_atm_fwd_rate.setter
    def swaption_atm_fwd_rate(self, value: float):
        self._property_changed('swaption_atm_fwd_rate')
        self.__swaption_atm_fwd_rate = value        

    @property
    def live_date(self) -> Union[Op, datetime.date]:
        return self.__live_date

    @live_date.setter
    def live_date(self, value: Union[Op, datetime.date]):
        self._property_changed('live_date')
        self.__live_date = value        

    @property
    def ask_high(self) -> float:
        """The highest Ask Price (price offering to sell)."""
        return self.__ask_high

    @ask_high.setter
    def ask_high(self, value: float):
        self._property_changed('ask_high')
        self.__ask_high = value        

    @property
    def corporate_action_type(self) -> str:
        """Different types of corporate actions from solactive"""
        return self.__corporate_action_type

    @corporate_action_type.setter
    def corporate_action_type(self, value: str):
        self._property_changed('corporate_action_type')
        self.__corporate_action_type = value        

    @property
    def prime_id(self) -> str:
        """Prime Id."""
        return self.__prime_id

    @prime_id.setter
    def prime_id(self, value: str):
        self._property_changed('prime_id')
        self.__prime_id = value        

    @property
    def region_name(self) -> str:
        """Name of the region for which FCI is calculated ??? Developed Markets, Emerging
           Markets, Euro Area, Global."""
        return self.__region_name

    @region_name.setter
    def region_name(self, value: str):
        self._property_changed('region_name')
        self.__region_name = value        

    @property
    def description(self) -> str:
        """Description of asset."""
        return self.__description

    @description.setter
    def description(self, value: str):
        self._property_changed('description')
        self.__description = value        

    @property
    def asset_classifications_is_country_primary(self) -> bool:
        """Whether or not it is the primary exchange asset for the exchange country."""
        return self.__asset_classifications_is_country_primary

    @asset_classifications_is_country_primary.setter
    def asset_classifications_is_country_primary(self, value: bool):
        self._property_changed('asset_classifications_is_country_primary')
        self.__asset_classifications_is_country_primary = value        

    @property
    def value_revised(self) -> str:
        """Revised value."""
        return self.__value_revised

    @value_revised.setter
    def value_revised(self, value: str):
        self._property_changed('value_revised')
        self.__value_revised = value        

    @property
    def adjusted_trade_price(self) -> float:
        """Last trade price or value adjusted for corporate actions."""
        return self.__adjusted_trade_price

    @adjusted_trade_price.setter
    def adjusted_trade_price(self, value: float):
        self._property_changed('adjusted_trade_price')
        self.__adjusted_trade_price = value        

    @property
    def forecast_time(self) -> datetime.datetime:
        """Time of forecasted electricity loads (in UTC)."""
        return self.__forecast_time

    @forecast_time.setter
    def forecast_time(self, value: datetime.datetime):
        self._property_changed('forecast_time')
        self.__forecast_time = value        

    @property
    def is_adr(self) -> bool:
        """Is ADR or not."""
        return self.__is_adr

    @is_adr.setter
    def is_adr(self, value: bool):
        self._property_changed('is_adr')
        self.__is_adr = value        

    @property
    def factor(self) -> str:
        """For Axioma, one of: Exchange Rate Sensitivity, Growth, Leverage, Medium-Term
           Momentum, Short-Term Momentum, Size, Value, Volatility. For Prime,
           one of: Long Concentration, Short Concentration, Long Crowdedness,
           Short Crowdedness, Crowdedness momentum, Short Conviction."""
        return self.__factor

    @factor.setter
    def factor(self, value: str):
        self._property_changed('factor')
        self.__factor = value        

    @property
    def days_on_loan(self) -> float:
        """The number of days this loan as been on our books."""
        return self.__days_on_loan

    @days_on_loan.setter
    def days_on_loan(self, value: float):
        self._property_changed('days_on_loan')
        self.__days_on_loan = value        

    @property
    def long_conviction_small(self) -> float:
        """The count of long ideas with small conviction."""
        return self.__long_conviction_small

    @long_conviction_small.setter
    def long_conviction_small(self, value: float):
        self._property_changed('long_conviction_small')
        self.__long_conviction_small = value        

    @property
    def service_id(self) -> str:
        """Service ID."""
        return self.__service_id

    @service_id.setter
    def service_id(self, value: str):
        self._property_changed('service_id')
        self.__service_id = value        

    @property
    def gsfeer(self) -> float:
        """Goldman Sachs Fundamental Equilibrium Exchange Rate."""
        return self.__gsfeer

    @gsfeer.setter
    def gsfeer(self, value: float):
        self._property_changed('gsfeer')
        self.__gsfeer = value        

    @property
    def wam(self) -> float:
        """Weighted average maturity, average of effective maturities of all securities
           held in portfolio, weighted."""
        return self.__wam

    @wam.setter
    def wam(self, value: float):
        self._property_changed('wam')
        self.__wam = value        

    @property
    def wal(self) -> float:
        """Weighted average life, measures sensitivity to changes in liquidity."""
        return self.__wal

    @wal.setter
    def wal(self, value: float):
        self._property_changed('wal')
        self.__wal = value        

    @property
    def backtest_id(self) -> str:
        """Marquee unique backtest identifier."""
        return self.__backtest_id

    @backtest_id.setter
    def backtest_id(self, value: str):
        self._property_changed('backtest_id')
        self.__backtest_id = value        

    @property
    def leg_two_index_location(self) -> str:
        """Location of leg."""
        return self.__leg_two_index_location

    @leg_two_index_location.setter
    def leg_two_index_location(self, value: str):
        self._property_changed('leg_two_index_location')
        self.__leg_two_index_location = value        

    @property
    def g_score(self) -> float:
        """Score for governance metrics."""
        return self.__g_score

    @g_score.setter
    def g_score(self, value: float):
        self._property_changed('g_score')
        self.__g_score = value        

    @property
    def corporate_spread_contribution(self) -> float:
        """Contribution of corporate spread component to FCI."""
        return self.__corporate_spread_contribution

    @corporate_spread_contribution.setter
    def corporate_spread_contribution(self, value: float):
        self._property_changed('corporate_spread_contribution')
        self.__corporate_spread_contribution = value        

    @property
    def market_value(self) -> float:
        """Marketable value of a given position, generally the market price for a given
           date."""
        return self.__market_value

    @market_value.setter
    def market_value(self, value: float):
        self._property_changed('market_value')
        self.__market_value = value        

    @property
    def notional_currency1(self) -> str:
        """An indication of the type of currency of the notional or principal amount."""
        return self.__notional_currency1

    @notional_currency1.setter
    def notional_currency1(self, value: str):
        self._property_changed('notional_currency1')
        self.__notional_currency1 = value        

    @property
    def net_debt_to_ebitda(self) -> float:
        """Net Debt to EBITDA."""
        return self.__net_debt_to_ebitda

    @net_debt_to_ebitda.setter
    def net_debt_to_ebitda(self, value: float):
        self._property_changed('net_debt_to_ebitda')
        self.__net_debt_to_ebitda = value        

    @property
    def notional_currency2(self) -> str:
        """Same as Notional Currency 1."""
        return self.__notional_currency2

    @notional_currency2.setter
    def notional_currency2(self, value: str):
        self._property_changed('notional_currency2')
        self.__notional_currency2 = value        

    @property
    def multiple_score(self) -> float:
        """Multiple percentile relative to Americas coverage universe (a higher score means
           more expensive)."""
        return self.__multiple_score

    @multiple_score.setter
    def multiple_score(self, value: float):
        self._property_changed('multiple_score')
        self.__multiple_score = value        

    @property
    def beta_adjusted_exposure(self) -> float:
        """Beta adjusted exposure."""
        return self.__beta_adjusted_exposure

    @beta_adjusted_exposure.setter
    def beta_adjusted_exposure(self, value: float):
        self._property_changed('beta_adjusted_exposure')
        self.__beta_adjusted_exposure = value        

    @property
    def paid(self) -> float:
        """Number of trades paid."""
        return self.__paid

    @paid.setter
    def paid(self, value: float):
        self._property_changed('paid')
        self.__paid = value        

    @property
    def short(self) -> float:
        """Short exposure."""
        return self.__short

    @short.setter
    def short(self, value: float):
        self._property_changed('short')
        self.__short = value        

    @property
    def bos_in_ticks_description(self) -> str:
        """Description of the Stock's Bid-Offer Spread in Ticks on the particular date."""
        return self.__bos_in_ticks_description

    @bos_in_ticks_description.setter
    def bos_in_ticks_description(self, value: str):
        self._property_changed('bos_in_ticks_description')
        self.__bos_in_ticks_description = value        

    @property
    def time(self) -> datetime.datetime:
        """ISO 8601 formatted date and time."""
        return self.__time

    @time.setter
    def time(self, value: datetime.datetime):
        self._property_changed('time')
        self.__time = value        

    @property
    def implied_correlation(self) -> float:
        """Correlation of an asset implied by observations of market prices."""
        return self.__implied_correlation

    @implied_correlation.setter
    def implied_correlation(self, value: float):
        self._property_changed('implied_correlation')
        self.__implied_correlation = value        

    @property
    def event_end_date_time(self) -> datetime.datetime:
        """The end time of the event if the event occurs during a time window and the event
           has a specific end time."""
        return self.__event_end_date_time

    @event_end_date_time.setter
    def event_end_date_time(self, value: datetime.datetime):
        self._property_changed('event_end_date_time')
        self.__event_end_date_time = value        

    @property
    def normalized_performance(self) -> float:
        """Performance that is normalized to 1."""
        return self.__normalized_performance

    @normalized_performance.setter
    def normalized_performance(self, value: float):
        self._property_changed('normalized_performance')
        self.__normalized_performance = value        

    @property
    def taxonomy(self) -> str:
        """An indication of the product taxonomy."""
        return self.__taxonomy

    @taxonomy.setter
    def taxonomy(self, value: str):
        self._property_changed('taxonomy')
        self.__taxonomy = value        

    @property
    def swaption_vol(self) -> float:
        """Historical implied normal volatility for a liquid point on swaption vol surface."""
        return self.__swaption_vol

    @swaption_vol.setter
    def swaption_vol(self, value: float):
        self._property_changed('swaption_vol')
        self.__swaption_vol = value        

    @property
    def source_origin(self) -> str:
        """Source origin."""
        return self.__source_origin

    @source_origin.setter
    def source_origin(self, value: str):
        self._property_changed('source_origin')
        self.__source_origin = value        

    @property
    def measures(self) -> Tuple[str, ...]:
        """Fields that are nullable."""
        return self.__measures

    @measures.setter
    def measures(self, value: Tuple[str, ...]):
        self._property_changed('measures')
        self.__measures = value        

    @property
    def total_quantity(self) -> float:
        """Rounded total quantity."""
        return self.__total_quantity

    @total_quantity.setter
    def total_quantity(self, value: float):
        self._property_changed('total_quantity')
        self.__total_quantity = value        

    @property
    def internal_user(self) -> bool:
        """Whether user is internal or not."""
        return self.__internal_user

    @internal_user.setter
    def internal_user(self, value: bool):
        self._property_changed('internal_user')
        self.__internal_user = value        

    @property
    def created_time(self) -> datetime.datetime:
        """Time created. ISO 8601 formatted string"""
        return self.__created_time

    @created_time.setter
    def created_time(self, value: datetime.datetime):
        self._property_changed('created_time')
        self.__created_time = value        

    @property
    def identifier(self) -> str:
        """Filter by any identifier of an asset like ticker, bloomberg id etc."""
        return self.__identifier

    @identifier.setter
    def identifier(self, value: str):
        self._property_changed('identifier')
        self.__identifier = value        

    @property
    def price_unit(self) -> str:
        """Unit of reported price."""
        return self.__price_unit

    @price_unit.setter
    def price_unit(self, value: str):
        self._property_changed('price_unit')
        self.__price_unit = value        

    @property
    def redemption_option(self) -> str:
        """Indicates the calculation convention for callable instruments."""
        return self.__redemption_option

    @redemption_option.setter
    def redemption_option(self, value: str):
        self._property_changed('redemption_option')
        self.__redemption_option = value        

    @property
    def notional_unit2(self) -> str:
        """Unit of reported notional price."""
        return self.__notional_unit2

    @notional_unit2.setter
    def notional_unit2(self, value: str):
        self._property_changed('notional_unit2')
        self.__notional_unit2 = value        

    @property
    def unadjusted_low(self) -> float:
        """Unadjusted low level of an asset based on official exchange fixing or
           calculation agent marked level."""
        return self.__unadjusted_low

    @unadjusted_low.setter
    def unadjusted_low(self, value: float):
        self._property_changed('unadjusted_low')
        self.__unadjusted_low = value        

    @property
    def notional_unit1(self) -> str:
        """Unit of reported notional price."""
        return self.__notional_unit1

    @notional_unit1.setter
    def notional_unit1(self, value: str):
        self._property_changed('notional_unit1')
        self.__notional_unit1 = value        

    @property
    def sedol(self) -> str:
        """SEDOL - Stock Exchange Daily Official List (subject to licensing)."""
        return self.__sedol

    @sedol.setter
    def sedol(self, value: str):
        self._property_changed('sedol')
        self.__sedol = value        

    @property
    def rounding_cost_pnl(self) -> float:
        """Rounding Cost Profit and Loss."""
        return self.__rounding_cost_pnl

    @rounding_cost_pnl.setter
    def rounding_cost_pnl(self, value: float):
        self._property_changed('rounding_cost_pnl')
        self.__rounding_cost_pnl = value        

    @property
    def sustain_global(self) -> bool:
        """True if the stock is on the SUSTAIN (Global) 50 list as of the corresponding
           date. False if the stock is removed from the SUSTAIN (Global) 50 list
           on the corresponding date."""
        return self.__sustain_global

    @sustain_global.setter
    def sustain_global(self, value: bool):
        self._property_changed('sustain_global')
        self.__sustain_global = value        

    @property
    def portfolio_id(self) -> str:
        """Marquee unique identifier for a portfolio."""
        return self.__portfolio_id

    @portfolio_id.setter
    def portfolio_id(self, value: str):
        self._property_changed('portfolio_id')
        self.__portfolio_id = value        

    @property
    def ending_date(self) -> str:
        """End date of the period the valuation refers to."""
        return self.__ending_date

    @ending_date.setter
    def ending_date(self, value: str):
        self._property_changed('ending_date')
        self.__ending_date = value        

    @property
    def cap_floor_atm_fwd_rate(self) -> float:
        """Cap Floor ATM forward rate."""
        return self.__cap_floor_atm_fwd_rate

    @cap_floor_atm_fwd_rate.setter
    def cap_floor_atm_fwd_rate(self, value: float):
        self._property_changed('cap_floor_atm_fwd_rate')
        self.__cap_floor_atm_fwd_rate = value        

    @property
    def es_percentile(self) -> float:
        """Sector relative percentile based on E&S score."""
        return self.__es_percentile

    @es_percentile.setter
    def es_percentile(self, value: float):
        self._property_changed('es_percentile')
        self.__es_percentile = value        

    @property
    def ann_return3_year(self) -> float:
        """Total return representing past performance, used for GS Money Market onshore
           funds, over three years."""
        return self.__ann_return3_year

    @ann_return3_year.setter
    def ann_return3_year(self, value: float):
        self._property_changed('ann_return3_year')
        self.__ann_return3_year = value        

    @property
    def rcic(self) -> str:
        """Reuters composite instrument code (subject to licensing)."""
        return self.__rcic

    @rcic.setter
    def rcic(self, value: str):
        self._property_changed('rcic')
        self.__rcic = value        

    @property
    def hit_rate_qtd(self) -> float:
        """Hit Rate Ratio Quarter to Date."""
        return self.__hit_rate_qtd

    @hit_rate_qtd.setter
    def hit_rate_qtd(self, value: float):
        self._property_changed('hit_rate_qtd')
        self.__hit_rate_qtd = value        

    @property
    def fci(self) -> float:
        """Nominal FCI value."""
        return self.__fci

    @fci.setter
    def fci(self, value: float):
        self._property_changed('fci')
        self.__fci = value        

    @property
    def recall_quantity(self) -> float:
        """Defines the amount of shares being recalled in a stock loan recall activity."""
        return self.__recall_quantity

    @recall_quantity.setter
    def recall_quantity(self, value: float):
        self._property_changed('recall_quantity')
        self.__recall_quantity = value        

    @property
    def premium(self) -> float:
        """An indication of the market value at the time of execution."""
        return self.__premium

    @premium.setter
    def premium(self, value: float):
        self._property_changed('premium')
        self.__premium = value        

    @property
    def low(self) -> float:
        """Low level of an asset based on official exchange fixing or calculation agent
           marked level."""
        return self.__low

    @low.setter
    def low(self, value: float):
        self._property_changed('low')
        self.__low = value        

    @property
    def cross_group(self) -> str:
        """Economic cross groupings."""
        return self.__cross_group

    @cross_group.setter
    def cross_group(self, value: str):
        self._property_changed('cross_group')
        self.__cross_group = value        

    @property
    def report_run_time(self) -> datetime.datetime:
        """Time that the report was run."""
        return self.__report_run_time

    @report_run_time.setter
    def report_run_time(self, value: datetime.datetime):
        self._property_changed('report_run_time')
        self.__report_run_time = value        

    @property
    def five_day_price_change_bps(self) -> float:
        """The five day movement in price measured in basis points."""
        return self.__five_day_price_change_bps

    @five_day_price_change_bps.setter
    def five_day_price_change_bps(self, value: float):
        self._property_changed('five_day_price_change_bps')
        self.__five_day_price_change_bps = value        

    @property
    def holdings(self) -> float:
        """Number of units of a given asset held within a portfolio."""
        return self.__holdings

    @holdings.setter
    def holdings(self, value: float):
        self._property_changed('holdings')
        self.__holdings = value        

    @property
    def price_method(self) -> str:
        """Method used to calculate net price."""
        return self.__price_method

    @price_method.setter
    def price_method(self, value: str):
        self._property_changed('price_method')
        self.__price_method = value        

    @property
    def mid_price(self) -> float:
        """The mid price."""
        return self.__mid_price

    @mid_price.setter
    def mid_price(self, value: float):
        self._property_changed('mid_price')
        self.__mid_price = value        

    @property
    def tcm_cost_horizon2_day(self) -> float:
        """TCM cost with a 2 day time horizon."""
        return self.__tcm_cost_horizon2_day

    @tcm_cost_horizon2_day.setter
    def tcm_cost_horizon2_day(self, value: float):
        self._property_changed('tcm_cost_horizon2_day')
        self.__tcm_cost_horizon2_day = value        

    @property
    def pending_loan_count(self) -> float:
        """The number of pending loans that exist on a given date."""
        return self.__pending_loan_count

    @pending_loan_count.setter
    def pending_loan_count(self, value: float):
        self._property_changed('pending_loan_count')
        self.__pending_loan_count = value        

    @property
    def price_spot_stop_loss_unit(self) -> str:
        """Unit in which the stop loss price is reported."""
        return self.__price_spot_stop_loss_unit

    @price_spot_stop_loss_unit.setter
    def price_spot_stop_loss_unit(self, value: str):
        self._property_changed('price_spot_stop_loss_unit')
        self.__price_spot_stop_loss_unit = value        

    @property
    def queue_in_lots(self) -> float:
        """The Queue size in Lots (if applicable) of the stock  on the particular date."""
        return self.__queue_in_lots

    @queue_in_lots.setter
    def queue_in_lots(self, value: float):
        self._property_changed('queue_in_lots')
        self.__queue_in_lots = value        

    @property
    def price_range_in_ticks_description(self) -> str:
        """Description of the Stock's Price Range in Ticks on the particular date."""
        return self.__price_range_in_ticks_description

    @price_range_in_ticks_description.setter
    def price_range_in_ticks_description(self, value: str):
        self._property_changed('price_range_in_ticks_description')
        self.__price_range_in_ticks_description = value        

    @property
    def tender_offer_expiration_date(self) -> str:
        """Expiration date of the tender offer."""
        return self.__tender_offer_expiration_date

    @tender_offer_expiration_date.setter
    def tender_offer_expiration_date(self, value: str):
        self._property_changed('tender_offer_expiration_date')
        self.__tender_offer_expiration_date = value        

    @property
    def primary_country_ric(self) -> str:
        """Reuters primary country instrument code (subject to licensing)."""
        return self.__primary_country_ric

    @primary_country_ric.setter
    def primary_country_ric(self, value: str):
        self._property_changed('primary_country_ric')
        self.__primary_country_ric = value        

    @property
    def leg_one_fixed_payment(self) -> float:
        """If fixed payment leg, the fixed payment amount, which is price*number of
           contracts bought*contract unit."""
        return self.__leg_one_fixed_payment

    @leg_one_fixed_payment.setter
    def leg_one_fixed_payment(self, value: float):
        self._property_changed('leg_one_fixed_payment')
        self.__leg_one_fixed_payment = value        

    @property
    def option_expiration_frequency(self) -> str:
        """Option Expiration Frequency provided by Participant (e.g., Daily, Monthly)."""
        return self.__option_expiration_frequency

    @option_expiration_frequency.setter
    def option_expiration_frequency(self, value: str):
        self._property_changed('option_expiration_frequency')
        self.__option_expiration_frequency = value        

    @property
    def lending_fund_nav_trend(self) -> float:
        """Net Asset Value trend of a securities lending fund."""
        return self.__lending_fund_nav_trend

    @lending_fund_nav_trend.setter
    def lending_fund_nav_trend(self, value: float):
        self._property_changed('lending_fund_nav_trend')
        self.__lending_fund_nav_trend = value        

    @property
    def tcm_cost_participation_rate5_pct(self) -> float:
        """TCM cost with a 5 percent participation rate."""
        return self.__tcm_cost_participation_rate5_pct

    @tcm_cost_participation_rate5_pct.setter
    def tcm_cost_participation_rate5_pct(self, value: float):
        self._property_changed('tcm_cost_participation_rate5_pct')
        self.__tcm_cost_participation_rate5_pct = value        

    @property
    def is_active(self) -> bool:
        """Whether this entry is active."""
        return self.__is_active

    @is_active.setter
    def is_active(self, value: bool):
        self._property_changed('is_active')
        self.__is_active = value        

    @property
    def growth_score(self) -> float:
        """Growth percentile relative to Americas coverage universe (a higher score means
           faster growth)."""
        return self.__growth_score

    @growth_score.setter
    def growth_score(self, value: float):
        self._property_changed('growth_score')
        self.__growth_score = value        

    @property
    def buffer_threshold(self) -> float:
        """The required buffer between holdings and on loan quantity for an asset."""
        return self.__buffer_threshold

    @buffer_threshold.setter
    def buffer_threshold(self, value: float):
        self._property_changed('buffer_threshold')
        self.__buffer_threshold = value        

    @property
    def price_forming_continuation_data(self) -> str:
        """An indication of whether an SB swap transaction is a post-execution event that
           affects the price of the swap transaction, e.g. terminations,
           assignments, novations, exchanges, transfers, amendments, conveyances
           or extinguishing of rights that change the price of the SB swap."""
        return self.__price_forming_continuation_data

    @price_forming_continuation_data.setter
    def price_forming_continuation_data(self, value: str):
        self._property_changed('price_forming_continuation_data')
        self.__price_forming_continuation_data = value        

    @property
    def adjusted_short_interest(self) -> float:
        """Adjusted Short Interest rate."""
        return self.__adjusted_short_interest

    @adjusted_short_interest.setter
    def adjusted_short_interest(self, value: float):
        self._property_changed('adjusted_short_interest')
        self.__adjusted_short_interest = value        

    @property
    def asset_parameters_strike(self) -> str:
        """Strike of the asset."""
        return self.__asset_parameters_strike

    @asset_parameters_strike.setter
    def asset_parameters_strike(self, value: str):
        self._property_changed('asset_parameters_strike')
        self.__asset_parameters_strike = value        

    @property
    def asset_parameters_termination_date(self) -> str:
        """Relative termination date."""
        return self.__asset_parameters_termination_date

    @asset_parameters_termination_date.setter
    def asset_parameters_termination_date(self, value: str):
        self._property_changed('asset_parameters_termination_date')
        self.__asset_parameters_termination_date = value        

    @property
    def estimated_spread(self) -> float:
        """Average bid-ask quoted spread of the stock (bps) over the execution horizon (1
           day)."""
        return self.__estimated_spread

    @estimated_spread.setter
    def estimated_spread(self, value: float):
        self._property_changed('estimated_spread')
        self.__estimated_spread = value        

    @property
    def asset_parameters_effective_date(self) -> str:
        """Relative effective date."""
        return self.__asset_parameters_effective_date

    @asset_parameters_effective_date.setter
    def asset_parameters_effective_date(self, value: str):
        self._property_changed('asset_parameters_effective_date')
        self.__asset_parameters_effective_date = value        

    @property
    def ann_return10_year(self) -> float:
        """Total return representing past performance, used for GS Money Market onshore
           funds, over ten years."""
        return self.__ann_return10_year

    @ann_return10_year.setter
    def ann_return10_year(self, value: float):
        self._property_changed('ann_return10_year')
        self.__ann_return10_year = value        

    @property
    def created(self) -> datetime.datetime:
        """Created time."""
        return self.__created

    @created.setter
    def created(self, value: datetime.datetime):
        self._property_changed('created')
        self.__created = value        

    @property
    def tcm_cost(self) -> float:
        """Pretrade computation of trading out cost."""
        return self.__tcm_cost

    @tcm_cost.setter
    def tcm_cost(self, value: float):
        self._property_changed('tcm_cost')
        self.__tcm_cost = value        

    @property
    def sustain_japan(self) -> bool:
        """True if the stock is on the SUSTAIN Japan list as of the corresponding date.
           False if the stock is removed from the SUSTAIN Japan list on the
           corresponding date."""
        return self.__sustain_japan

    @sustain_japan.setter
    def sustain_japan(self, value: bool):
        self._property_changed('sustain_japan')
        self.__sustain_japan = value        

    @property
    def fixed_payment_currency_leg1(self) -> str:
        """If fixed payment leg, the unit of fixed payment."""
        return self.__fixed_payment_currency_leg1

    @fixed_payment_currency_leg1.setter
    def fixed_payment_currency_leg1(self, value: str):
        self._property_changed('fixed_payment_currency_leg1')
        self.__fixed_payment_currency_leg1 = value        

    @property
    def hedge_tracking_error(self) -> float:
        """Standard deviation of the difference in the portfolio and benchmark returns over
           time."""
        return self.__hedge_tracking_error

    @hedge_tracking_error.setter
    def hedge_tracking_error(self, value: float):
        self._property_changed('hedge_tracking_error')
        self.__hedge_tracking_error = value        

    @property
    def fixed_payment_currency_leg2(self) -> str:
        """If fixed payment leg, the unit of fixed payment."""
        return self.__fixed_payment_currency_leg2

    @fixed_payment_currency_leg2.setter
    def fixed_payment_currency_leg2(self, value: str):
        self._property_changed('fixed_payment_currency_leg2')
        self.__fixed_payment_currency_leg2 = value        

    @property
    def market_cap_category(self) -> str:
        """Category of market capitalizations a fund is focused on from an investment
           perspective. Same view permissions as the asset."""
        return self.__market_cap_category

    @market_cap_category.setter
    def market_cap_category(self, value: str):
        self._property_changed('market_cap_category')
        self.__market_cap_category = value        

    @property
    def historical_volume(self) -> float:
        """One month rolling average."""
        return self.__historical_volume

    @historical_volume.setter
    def historical_volume(self, value: float):
        self._property_changed('historical_volume')
        self.__historical_volume = value        

    @property
    def strike_price(self) -> float:
        """Strike price."""
        return self.__strike_price

    @strike_price.setter
    def strike_price(self, value: float):
        self._property_changed('strike_price')
        self.__strike_price = value        

    @property
    def event_start_date(self) -> datetime.date:
        """The start date of the event if the event occurs during a time window, in the
           time zone of the exchange where the company is listed (optional)."""
        return self.__event_start_date

    @event_start_date.setter
    def event_start_date(self, value: datetime.date):
        self._property_changed('event_start_date')
        self.__event_start_date = value        

    @property
    def reset_frequency_leg1(self) -> str:
        """An integer multiplier of a period describing how often the parties to an SB swap
           transaction shall evaluate and, when applicable, change the price
           used for the underlying assets of the swap transaction (leg 1). Such
           reset frequency may be described as one letter preceded by an
           integer."""
        return self.__reset_frequency_leg1

    @reset_frequency_leg1.setter
    def reset_frequency_leg1(self, value: str):
        self._property_changed('reset_frequency_leg1')
        self.__reset_frequency_leg1 = value        

    @property
    def reset_frequency_leg2(self) -> str:
        """An integer multiplier of a period describing how often the parties to an SB swap
           transaction shall evaluate and, when applicable, change the price
           used for the underlying assets of the swap transaction (leg 2). Such
           reset frequency may be described as one letter preceded by an
           integer."""
        return self.__reset_frequency_leg2

    @reset_frequency_leg2.setter
    def reset_frequency_leg2(self, value: str):
        self._property_changed('reset_frequency_leg2')
        self.__reset_frequency_leg2 = value        

    @property
    def equity_gamma(self) -> float:
        """Gamma exposure to equity products."""
        return self.__equity_gamma

    @equity_gamma.setter
    def equity_gamma(self, value: float):
        self._property_changed('equity_gamma')
        self.__equity_gamma = value        

    @property
    def gross_income(self) -> float:
        """The income earned by the reinvested collateral including the rebate or fee,
           excluding lender or partner fees."""
        return self.__gross_income

    @gross_income.setter
    def gross_income(self, value: float):
        self._property_changed('gross_income')
        self.__gross_income = value        

    @property
    def adjusted_open_price(self) -> float:
        """Opening level of an asset based on official exchange fixing or calculation agent
           marked level adjusted for corporate actions."""
        return self.__adjusted_open_price

    @adjusted_open_price.setter
    def adjusted_open_price(self, value: float):
        self._property_changed('adjusted_open_price')
        self.__adjusted_open_price = value        

    @property
    def asset_count_in_model(self) -> float:
        """Number of assets in a portfolio in a given risk model."""
        return self.__asset_count_in_model

    @asset_count_in_model.setter
    def asset_count_in_model(self, value: float):
        self._property_changed('asset_count_in_model')
        self.__asset_count_in_model = value        

    @property
    def country_id(self) -> str:
        """Marquee country object identifier."""
        return self.__country_id

    @country_id.setter
    def country_id(self, value: str):
        self._property_changed('country_id')
        self.__country_id = value        

    @property
    def total_returns(self) -> float:
        """Total returns for backtest."""
        return self.__total_returns

    @total_returns.setter
    def total_returns(self, value: float):
        self._property_changed('total_returns')
        self.__total_returns = value        

    @property
    def lender(self) -> str:
        """Name of the lending entity on a securities lending agreement."""
        return self.__lender

    @lender.setter
    def lender(self, value: str):
        self._property_changed('lender')
        self.__lender = value        

    @property
    def ann_return1_year(self) -> float:
        """Total return representing past performance, used for GS Money Market onshore
           funds over one year."""
        return self.__ann_return1_year

    @ann_return1_year.setter
    def ann_return1_year(self, value: float):
        self._property_changed('ann_return1_year')
        self.__ann_return1_year = value        

    @property
    def min_temperature(self) -> float:
        """Minimum temperature observed on a given day in fahrenheit."""
        return self.__min_temperature

    @min_temperature.setter
    def min_temperature(self, value: float):
        self._property_changed('min_temperature')
        self.__min_temperature = value        

    @property
    def eff_yield7_day(self) -> float:
        """Average income return over the previous 7 days reduced by any capital gains that
           may have been included in rate calculation, assuming the rate stays
           the same for one year and that dividends are reinvested."""
        return self.__eff_yield7_day

    @eff_yield7_day.setter
    def eff_yield7_day(self, value: float):
        self._property_changed('eff_yield7_day')
        self.__eff_yield7_day = value        

    @property
    def meeting_date(self) -> str:
        """Date the Central bank Meeting took place."""
        return self.__meeting_date

    @meeting_date.setter
    def meeting_date(self, value: str):
        self._property_changed('meeting_date')
        self.__meeting_date = value        

    @property
    def close_time(self) -> datetime.datetime:
        """Time closed. ISO 8601 formatted string."""
        return self.__close_time

    @close_time.setter
    def close_time(self, value: datetime.datetime):
        self._property_changed('close_time')
        self.__close_time = value        

    @property
    def amount(self) -> float:
        """Amount corporate actions pay out."""
        return self.__amount

    @amount.setter
    def amount(self, value: float):
        self._property_changed('amount')
        self.__amount = value        

    @property
    def lending_fund_acct(self) -> str:
        """Account associated with the securities lending fund."""
        return self.__lending_fund_acct

    @lending_fund_acct.setter
    def lending_fund_acct(self, value: str):
        self._property_changed('lending_fund_acct')
        self.__lending_fund_acct = value        

    @property
    def rebate(self) -> float:
        """Amount of the payment to an investor who puts up collateral in borrowing a
           stock."""
        return self.__rebate

    @rebate.setter
    def rebate(self, value: float):
        self._property_changed('rebate')
        self.__rebate = value        

    @property
    def flagship(self) -> bool:
        """Whether or not it is a flagship basket."""
        return self.__flagship

    @flagship.setter
    def flagship(self, value: bool):
        self._property_changed('flagship')
        self.__flagship = value        

    @property
    def additional_price_notation(self) -> float:
        """The additional price notation value includes execution events, the presence of
           collateral, frontend payments, back-end payments, or other
           noneconomic characteristics (e.g. counterparty credit risk) not
           illustrated in the reporting field for pricing characteristic."""
        return self.__additional_price_notation

    @additional_price_notation.setter
    def additional_price_notation(self, value: float):
        self._property_changed('additional_price_notation')
        self.__additional_price_notation = value        

    @property
    def election_type(self) -> str:
        """Type of election e.g. presidential."""
        return self.__election_type

    @election_type.setter
    def election_type(self, value: str):
        self._property_changed('election_type')
        self.__election_type = value        

    @property
    def implied_volatility(self) -> float:
        """Volatility of an asset implied by observations of market prices."""
        return self.__implied_volatility

    @implied_volatility.setter
    def implied_volatility(self, value: float):
        self._property_changed('implied_volatility')
        self.__implied_volatility = value        

    @property
    def spread(self) -> float:
        """Quoted (running) spread (mid) of buying / selling protection on an index.
           (Equally weighted CDS basket). In basis points."""
        return self.__spread

    @spread.setter
    def spread(self, value: float):
        self._property_changed('spread')
        self.__spread = value        

    @property
    def equity_delta(self) -> float:
        """Delta exposure to equity products."""
        return self.__equity_delta

    @equity_delta.setter
    def equity_delta(self, value: float):
        self._property_changed('equity_delta')
        self.__equity_delta = value        

    @property
    def gross_weight(self) -> float:
        """Sum of the absolute weight values, which equals the sum of absolute long and
           short weights. If you have IBM stock with shortWeight 0.2 and also
           IBM stock with longWeight 0.4, then the grossWeight would be 0.6
           (0.2+0.4)."""
        return self.__gross_weight

    @gross_weight.setter
    def gross_weight(self, value: float):
        self._property_changed('gross_weight')
        self.__gross_weight = value        

    @property
    def listed(self) -> bool:
        """Whether the asset is listed or not."""
        return self.__listed

    @listed.setter
    def listed(self, value: bool):
        self._property_changed('listed')
        self.__listed = value        

    @property
    def earnings_record_type(self) -> str:
        """The violation status for this particular line item."""
        return self.__earnings_record_type

    @earnings_record_type.setter
    def earnings_record_type(self, value: str):
        self._property_changed('earnings_record_type')
        self.__earnings_record_type = value        

    @property
    def g10_currency(self) -> bool:
        """Is a G10 asset."""
        return self.__g10_currency

    @g10_currency.setter
    def g10_currency(self, value: bool):
        self._property_changed('g10_currency')
        self.__g10_currency = value        

    @property
    def shock_style(self) -> str:
        """Style of shocks to be used."""
        return self.__shock_style

    @shock_style.setter
    def shock_style(self, value: str):
        self._property_changed('shock_style')
        self.__shock_style = value        

    @property
    def relative_period(self) -> str:
        """The relative period forward for which the forecast is available."""
        return self.__relative_period

    @relative_period.setter
    def relative_period(self, value: str):
        self._property_changed('relative_period')
        self.__relative_period = value        

    @property
    def methodology(self) -> str:
        """Methodology of dataset."""
        return self.__methodology

    @methodology.setter
    def methodology(self, value: str):
        self._property_changed('methodology')
        self.__methodology = value        

    @property
    def queue_clock_time_label(self):
        return self.__queue_clock_time_label

    @queue_clock_time_label.setter
    def queue_clock_time_label(self, value):
        self._property_changed('queue_clock_time_label')
        self.__queue_clock_time_label = value        

    @property
    def market_pnl(self) -> float:
        """Market Profit and Loss (PNL)."""
        return self.__market_pnl

    @market_pnl.setter
    def market_pnl(self, value: float):
        self._property_changed('market_pnl')
        self.__market_pnl = value        

    @property
    def sustain_asia_ex_japan(self) -> bool:
        """True if the stock is on the SUSTAIN Asia Ex Japan list as of the corresponding
           date. False if the stock is removed from the SUSTAIN Asia Ex Japan
           list on the corresponding date."""
        return self.__sustain_asia_ex_japan

    @sustain_asia_ex_japan.setter
    def sustain_asia_ex_japan(self, value: bool):
        self._property_changed('sustain_asia_ex_japan')
        self.__sustain_asia_ex_japan = value        

    @property
    def index_leg2(self) -> str:
        """If floating index leg, the index."""
        return self.__index_leg2

    @index_leg2.setter
    def index_leg2(self, value: str):
        self._property_changed('index_leg2')
        self.__index_leg2 = value        

    @property
    def index_leg1(self) -> str:
        """If floating index leg, the index."""
        return self.__index_leg1

    @index_leg1.setter
    def index_leg1(self, value: str):
        self._property_changed('index_leg1')
        self.__index_leg1 = value        

    @property
    def swap_rate(self) -> float:
        """ATM fixed rate for a benchmark tenor on a currency's fixed-floating swap curve."""
        return self.__swap_rate

    @swap_rate.setter
    def swap_rate(self, value: float):
        self._property_changed('swap_rate')
        self.__swap_rate = value        

    @property
    def mixed_swap_other_reported_sdr(self) -> str:
        """Indicates the other SDR to which a mixed swap is reported."""
        return self.__mixed_swap_other_reported_sdr

    @mixed_swap_other_reported_sdr.setter
    def mixed_swap_other_reported_sdr(self, value: str):
        self._property_changed('mixed_swap_other_reported_sdr')
        self.__mixed_swap_other_reported_sdr = value        

    @property
    def data_set_category(self) -> str:
        """Top level grouping of dataset."""
        return self.__data_set_category

    @data_set_category.setter
    def data_set_category(self, value: str):
        self._property_changed('data_set_category')
        self.__data_set_category = value        

    @property
    def bos_in_bps_label(self):
        return self.__bos_in_bps_label

    @bos_in_bps_label.setter
    def bos_in_bps_label(self, value):
        self._property_changed('bos_in_bps_label')
        self.__bos_in_bps_label = value        

    @property
    def bos_in_bps(self) -> float:
        """The Bid-Offer Spread of the stock in Basis points on the particular date."""
        return self.__bos_in_bps

    @bos_in_bps.setter
    def bos_in_bps(self, value: float):
        self._property_changed('bos_in_bps')
        self.__bos_in_bps = value        

    @property
    def fx_spot(self) -> float:
        """FX spot rate as determined by fixing source."""
        return self.__fx_spot

    @fx_spot.setter
    def fx_spot(self, value: float):
        self._property_changed('fx_spot')
        self.__fx_spot = value        

    @property
    def bid_low(self) -> float:
        """Lowest Bid Price (price willing to buy)."""
        return self.__bid_low

    @bid_low.setter
    def bid_low(self, value: float):
        self._property_changed('bid_low')
        self.__bid_low = value        

    @property
    def restrict_named_individuals(self) -> bool:
        """Restricts Visbility to Named Individuals."""
        return self.__restrict_named_individuals

    @restrict_named_individuals.setter
    def restrict_named_individuals(self, value: bool):
        self._property_changed('restrict_named_individuals')
        self.__restrict_named_individuals = value        

    @property
    def fair_variance_volatility(self) -> float:
        """The strike in volatility terms, calculated as square root of fair variance."""
        return self.__fair_variance_volatility

    @fair_variance_volatility.setter
    def fair_variance_volatility(self, value: float):
        self._property_changed('fair_variance_volatility')
        self.__fair_variance_volatility = value        

    @property
    def hedge_volatility(self) -> float:
        """Standard deviation of the annualized returns."""
        return self.__hedge_volatility

    @hedge_volatility.setter
    def hedge_volatility(self, value: float):
        self._property_changed('hedge_volatility')
        self.__hedge_volatility = value        

    @property
    def tags(self) -> Tuple[str, ...]:
        """Metadata associated with the object"""
        return self.__tags

    @tags.setter
    def tags(self, value: Tuple[str, ...]):
        self._property_changed('tags')
        self.__tags = value        

    @property
    def real_long_rates_contribution(self) -> float:
        """Contribution of long rate component to real FCI."""
        return self.__real_long_rates_contribution

    @real_long_rates_contribution.setter
    def real_long_rates_contribution(self, value: float):
        self._property_changed('real_long_rates_contribution')
        self.__real_long_rates_contribution = value        

    @property
    def client_exposure(self) -> float:
        """Exposure of client positions to the factor in percent of equity."""
        return self.__client_exposure

    @client_exposure.setter
    def client_exposure(self, value: float):
        self._property_changed('client_exposure')
        self.__client_exposure = value        

    @property
    def gs_sustain_sub_sector(self) -> str:
        """GS SUSTAIN sector."""
        return self.__gs_sustain_sub_sector

    @gs_sustain_sub_sector.setter
    def gs_sustain_sub_sector(self, value: str):
        self._property_changed('gs_sustain_sub_sector')
        self.__gs_sustain_sub_sector = value        

    @property
    def domain(self) -> str:
        """Domain that request came from."""
        return self.__domain

    @domain.setter
    def domain(self, value: str):
        self._property_changed('domain')
        self.__domain = value        

    @property
    def share_class_assets(self) -> float:
        """Total amount of assets under management in this shareclass."""
        return self.__share_class_assets

    @share_class_assets.setter
    def share_class_assets(self, value: float):
        self._property_changed('share_class_assets')
        self.__share_class_assets = value        

    @property
    def annuity(self) -> float:
        """Local currency annuity."""
        return self.__annuity

    @annuity.setter
    def annuity(self, value: float):
        self._property_changed('annuity')
        self.__annuity = value        

    @property
    def uid(self) -> str:
        """Two-digit code for countries and regions for which FCI numbers are represented.
           For countries it is the ISO 3166 2-digit country code. Regions are
           denoted as DM (Developed Markets), EM (Emerging Markets), EA (Euro
           Area) and GL (Global)."""
        return self.__uid

    @uid.setter
    def uid(self, value: str):
        self._property_changed('uid')
        self.__uid = value        

    @property
    def es_policy_percentile(self) -> float:
        """Sector relative percentile based on E&S policy score."""
        return self.__es_policy_percentile

    @es_policy_percentile.setter
    def es_policy_percentile(self, value: float):
        self._property_changed('es_policy_percentile')
        self.__es_policy_percentile = value        

    @property
    def floating_rate_option(self) -> str:
        """The underlying benchmark for the floating rate, e.g. USD-LIBOR-BBA, EUR-EURIBOR-
           TELERATE."""
        return self.__floating_rate_option

    @floating_rate_option.setter
    def floating_rate_option(self, value: str):
        self._property_changed('floating_rate_option')
        self.__floating_rate_option = value        

    @property
    def term(self) -> str:
        """Allowed risk model terms"""
        return self.__term

    @term.setter
    def term(self, value: str):
        self._property_changed('term')
        self.__term = value        

    @property
    def restrict_internal_gs_ntk(self) -> bool:
        """Restricts Internal Visibility to Data Beyond GS NTK."""
        return self.__restrict_internal_gs_ntk

    @restrict_internal_gs_ntk.setter
    def restrict_internal_gs_ntk(self, value: bool):
        self._property_changed('restrict_internal_gs_ntk')
        self.__restrict_internal_gs_ntk = value        

    @property
    def asset_parameters_clearing_house(self) -> str:
        """Clearing house."""
        return self.__asset_parameters_clearing_house

    @asset_parameters_clearing_house.setter
    def asset_parameters_clearing_house(self, value: str):
        self._property_changed('asset_parameters_clearing_house')
        self.__asset_parameters_clearing_house = value        

    @property
    def tcm_cost_participation_rate100_pct(self) -> float:
        """TCM cost with a 100 percent participation rate."""
        return self.__tcm_cost_participation_rate100_pct

    @tcm_cost_participation_rate100_pct.setter
    def tcm_cost_participation_rate100_pct(self, value: float):
        self._property_changed('tcm_cost_participation_rate100_pct')
        self.__tcm_cost_participation_rate100_pct = value        

    @property
    def disclaimer(self) -> str:
        """The legal disclaimer associated with the record."""
        return self.__disclaimer

    @disclaimer.setter
    def disclaimer(self, value: str):
        self._property_changed('disclaimer')
        self.__disclaimer = value        

    @property
    def measure_idx(self) -> int:
        """The index of the corresponding measure in the risk request."""
        return self.__measure_idx

    @measure_idx.setter
    def measure_idx(self, value: int):
        self._property_changed('measure_idx')
        self.__measure_idx = value        

    @property
    def loan_fee(self) -> float:
        """Fee charged for the loan of securities to a borrower in a securities lending
           agreement."""
        return self.__loan_fee

    @loan_fee.setter
    def loan_fee(self, value: float):
        self._property_changed('loan_fee')
        self.__loan_fee = value        

    @property
    def deployment_version(self) -> str:
        """Deployment version."""
        return self.__deployment_version

    @deployment_version.setter
    def deployment_version(self, value: str):
        self._property_changed('deployment_version')
        self.__deployment_version = value        

    @property
    def twi_contribution(self) -> float:
        """Contribution of trade weighted exchange rate index component to FCI."""
        return self.__twi_contribution

    @twi_contribution.setter
    def twi_contribution(self, value: float):
        self._property_changed('twi_contribution')
        self.__twi_contribution = value        

    @property
    def delisted(self) -> str:
        """Whether the security has been delisted."""
        return self.__delisted

    @delisted.setter
    def delisted(self, value: str):
        self._property_changed('delisted')
        self.__delisted = value        

    @property
    def regional_focus(self) -> str:
        """Section of the world a fund is focused on from an investment perspective. Same
           view permissions as the asset."""
        return self.__regional_focus

    @regional_focus.setter
    def regional_focus(self, value: str):
        self._property_changed('regional_focus')
        self.__regional_focus = value        

    @property
    def volume_primary(self) -> float:
        """Accumulated number of shares, lots or contracts traded according to the market
           convention at the primary exchange."""
        return self.__volume_primary

    @volume_primary.setter
    def volume_primary(self, value: float):
        self._property_changed('volume_primary')
        self.__volume_primary = value        

    @property
    def leg_two_delivery_point(self) -> str:
        """Delivery point of leg."""
        return self.__leg_two_delivery_point

    @leg_two_delivery_point.setter
    def leg_two_delivery_point(self, value: str):
        self._property_changed('leg_two_delivery_point')
        self.__leg_two_delivery_point = value        

    @property
    def funding_bid_price(self) -> float:
        """Latest Bid Price (price willing to buy)."""
        return self.__funding_bid_price

    @funding_bid_price.setter
    def funding_bid_price(self, value: float):
        self._property_changed('funding_bid_price')
        self.__funding_bid_price = value        

    @property
    def price_to_sales(self) -> float:
        """Price to sales."""
        return self.__price_to_sales

    @price_to_sales.setter
    def price_to_sales(self, value: float):
        self._property_changed('price_to_sales')
        self.__price_to_sales = value        

    @property
    def closing_auction(self) -> float:
        """Goldman's rate for trades on the closing auction."""
        return self.__closing_auction

    @closing_auction.setter
    def closing_auction(self, value: float):
        self._property_changed('closing_auction')
        self.__closing_auction = value        

    @property
    def new_ideas_qtd(self) -> float:
        """Ideas received by clients Quarter to date."""
        return self.__new_ideas_qtd

    @new_ideas_qtd.setter
    def new_ideas_qtd(self, value: float):
        self._property_changed('new_ideas_qtd')
        self.__new_ideas_qtd = value        

    @property
    def adjusted_ask_price(self) -> float:
        """Latest Ask Price (price offering to sell) adjusted for corporate actions."""
        return self.__adjusted_ask_price

    @adjusted_ask_price.setter
    def adjusted_ask_price(self, value: float):
        self._property_changed('adjusted_ask_price')
        self.__adjusted_ask_price = value        

    @property
    def quarter(self) -> str:
        """Quarter of forecast."""
        return self.__quarter

    @quarter.setter
    def quarter(self, value: str):
        self._property_changed('quarter')
        self.__quarter = value        

    @property
    def factor_universe(self) -> str:
        """Factor universe."""
        return self.__factor_universe

    @factor_universe.setter
    def factor_universe(self, value: str):
        self._property_changed('factor_universe')
        self.__factor_universe = value        

    @property
    def asset_parameters_floating_rate_option(self) -> str:
        """The underlying benchmark for the floating rate, e.g. USD-LIBOR-BBA, EUR-EURIBOR-
           TELERATE."""
        return self.__asset_parameters_floating_rate_option

    @asset_parameters_floating_rate_option.setter
    def asset_parameters_floating_rate_option(self, value: str):
        self._property_changed('asset_parameters_floating_rate_option')
        self.__asset_parameters_floating_rate_option = value        

    @property
    def arrival_rt(self) -> float:
        """Arrival Realtime."""
        return self.__arrival_rt

    @arrival_rt.setter
    def arrival_rt(self, value: float):
        self._property_changed('arrival_rt')
        self.__arrival_rt = value        

    @property
    def vote_share(self) -> float:
        """Vote share (predicted) in election."""
        return self.__vote_share

    @vote_share.setter
    def vote_share(self, value: float):
        self._property_changed('vote_share')
        self.__vote_share = value        

    @property
    def excess_margin_value(self) -> float:
        """Available credit value."""
        return self.__excess_margin_value

    @excess_margin_value.setter
    def excess_margin_value(self, value: float):
        self._property_changed('excess_margin_value')
        self.__excess_margin_value = value        

    @property
    def transaction_cost(self) -> float:
        """Transaction cost."""
        return self.__transaction_cost

    @transaction_cost.setter
    def transaction_cost(self, value: float):
        self._property_changed('transaction_cost')
        self.__transaction_cost = value        

    @property
    def central_bank_swap_rate(self) -> float:
        """Returns the OIS swap rate for a swap structured between consecutive meeting
           dates."""
        return self.__central_bank_swap_rate

    @central_bank_swap_rate.setter
    def central_bank_swap_rate(self, value: float):
        self._property_changed('central_bank_swap_rate')
        self.__central_bank_swap_rate = value        

    @property
    def servicing_cost_short_pnl(self) -> float:
        """Servicing Cost Short Profit and Loss."""
        return self.__servicing_cost_short_pnl

    @servicing_cost_short_pnl.setter
    def servicing_cost_short_pnl(self, value: float):
        self._property_changed('servicing_cost_short_pnl')
        self.__servicing_cost_short_pnl = value        

    @property
    def notional_unit_leg1(self) -> str:
        """Unit of reported notional price on leg 1."""
        return self.__notional_unit_leg1

    @notional_unit_leg1.setter
    def notional_unit_leg1(self, value: str):
        self._property_changed('notional_unit_leg1')
        self.__notional_unit_leg1 = value        

    @property
    def cluster_description(self) -> str:
        """Description of the Cluster characteristics."""
        return self.__cluster_description

    @cluster_description.setter
    def cluster_description(self, value: str):
        self._property_changed('cluster_description')
        self.__cluster_description = value        

    @property
    def notional_unit_leg2(self) -> str:
        """Unit of reported notional price on leg 2."""
        return self.__notional_unit_leg2

    @notional_unit_leg2.setter
    def notional_unit_leg2(self, value: str):
        self._property_changed('notional_unit_leg2')
        self.__notional_unit_leg2 = value        

    @property
    def position_amount(self) -> float:
        """Corporate actions amount * shares."""
        return self.__position_amount

    @position_amount.setter
    def position_amount(self, value: float):
        self._property_changed('position_amount')
        self.__position_amount = value        

    @property
    def wind_speed(self) -> float:
        """Average wind speed in knots."""
        return self.__wind_speed

    @wind_speed.setter
    def wind_speed(self, value: float):
        self._property_changed('wind_speed')
        self.__wind_speed = value        

    @property
    def event_start_date_time(self) -> datetime.datetime:
        """The start time of the event if the event occurs during a time window and the
           event has a specific start time, using UTC convention (optional)."""
        return self.__event_start_date_time

    @event_start_date_time.setter
    def event_start_date_time(self, value: datetime.datetime):
        self._property_changed('event_start_date_time')
        self.__event_start_date_time = value        

    @property
    def borrower_id(self) -> str:
        """Id of the borrowing entity on a securities lending agreement."""
        return self.__borrower_id

    @borrower_id.setter
    def borrower_id(self, value: str):
        self._property_changed('borrower_id')
        self.__borrower_id = value        

    @property
    def data_product(self) -> str:
        """Product that dataset belongs to."""
        return self.__data_product

    @data_product.setter
    def data_product(self, value: str):
        self._property_changed('data_product')
        self.__data_product = value        

    @property
    def implied_volatility_by_delta_strike(self) -> float:
        """Volatility of an asset implied by observations of market prices."""
        return self.__implied_volatility_by_delta_strike

    @implied_volatility_by_delta_strike.setter
    def implied_volatility_by_delta_strike(self, value: float):
        self._property_changed('implied_volatility_by_delta_strike')
        self.__implied_volatility_by_delta_strike = value        

    @property
    def bm_prime_id(self) -> float:
        """Benchmark prime ID of the treasury."""
        return self.__bm_prime_id

    @bm_prime_id.setter
    def bm_prime_id(self, value: float):
        self._property_changed('bm_prime_id')
        self.__bm_prime_id = value        

    @property
    def corporate_action(self) -> bool:
        """Whether or not it is a corporate action."""
        return self.__corporate_action

    @corporate_action.setter
    def corporate_action(self, value: bool):
        self._property_changed('corporate_action')
        self.__corporate_action = value        

    @property
    def conviction(self) -> str:
        """Confidence level in the trade idea."""
        return self.__conviction

    @conviction.setter
    def conviction(self, value: str):
        self._property_changed('conviction')
        self.__conviction = value        

    @property
    def gross_flow_normalized(self) -> float:
        """Gross flow for the asset divided by average in defined history."""
        return self.__gross_flow_normalized

    @gross_flow_normalized.setter
    def gross_flow_normalized(self, value: float):
        self._property_changed('gross_flow_normalized')
        self.__gross_flow_normalized = value        

    @property
    def g_regional_score(self) -> float:
        """A company???s score for G metrics within its region."""
        return self.__g_regional_score

    @g_regional_score.setter
    def g_regional_score(self, value: float):
        self._property_changed('g_regional_score')
        self.__g_regional_score = value        

    @property
    def factor_id(self) -> str:
        """Id for Factors."""
        return self.__factor_id

    @factor_id.setter
    def factor_id(self, value: str):
        self._property_changed('factor_id')
        self.__factor_id = value        

    @property
    def hard_to_borrow(self) -> bool:
        """Whether or not an asset is hard to borrow."""
        return self.__hard_to_borrow

    @hard_to_borrow.setter
    def hard_to_borrow(self, value: bool):
        self._property_changed('hard_to_borrow')
        self.__hard_to_borrow = value        

    @property
    def wpk(self) -> str:
        """Wertpapierkennnummer (WKN, WPKN, Wert), German security identifier code (subject
           to licensing)."""
        return self.__wpk

    @wpk.setter
    def wpk(self, value: str):
        self._property_changed('wpk')
        self.__wpk = value        

    @property
    def bid_change(self) -> float:
        """Change in BID price."""
        return self.__bid_change

    @bid_change.setter
    def bid_change(self, value: float):
        self._property_changed('bid_change')
        self.__bid_change = value        

    @property
    def month(self) -> str:
        """Month in YYYYMM format."""
        return self.__month

    @month.setter
    def month(self, value: str):
        self._property_changed('month')
        self.__month = value        

    @property
    def asset_parameters_expiration_date(self) -> str:
        """Relative expiration date."""
        return self.__asset_parameters_expiration_date

    @asset_parameters_expiration_date.setter
    def asset_parameters_expiration_date(self, value: str):
        self._property_changed('asset_parameters_expiration_date')
        self.__asset_parameters_expiration_date = value        

    @property
    def expiration(self) -> str:
        """The expiration date of the associated contract and the last date it trades."""
        return self.__expiration

    @expiration.setter
    def expiration(self, value: str):
        self._property_changed('expiration')
        self.__expiration = value        

    @property
    def country_name(self) -> str:
        """Country name for which FCI is calculated."""
        return self.__country_name

    @country_name.setter
    def country_name(self, value: str):
        self._property_changed('country_name')
        self.__country_name = value        

    @property
    def starting_date(self) -> str:
        """Start date of the period the valuation refers to."""
        return self.__starting_date

    @starting_date.setter
    def starting_date(self, value: str):
        self._property_changed('starting_date')
        self.__starting_date = value        

    @property
    def onboarded(self) -> bool:
        """Whether or not social domain has been onboarded."""
        return self.__onboarded

    @onboarded.setter
    def onboarded(self, value: bool):
        self._property_changed('onboarded')
        self.__onboarded = value        

    @property
    def liquidity_score(self) -> float:
        """Liquidity conditions in the aggregate market, calculated as the average of touch
           liquidity score, touch spread score, and depth spread score."""
        return self.__liquidity_score

    @liquidity_score.setter
    def liquidity_score(self, value: float):
        self._property_changed('liquidity_score')
        self.__liquidity_score = value        

    @property
    def spread_leg2(self) -> float:
        """Spread of leg."""
        return self.__spread_leg2

    @spread_leg2.setter
    def spread_leg2(self, value: float):
        self._property_changed('spread_leg2')
        self.__spread_leg2 = value        

    @property
    def spread_leg1(self) -> float:
        """Spread of leg."""
        return self.__spread_leg1

    @spread_leg1.setter
    def spread_leg1(self, value: float):
        self._property_changed('spread_leg1')
        self.__spread_leg1 = value        

    @property
    def long_rates_contribution(self) -> float:
        """Contribution of long rate component to FCI."""
        return self.__long_rates_contribution

    @long_rates_contribution.setter
    def long_rates_contribution(self, value: float):
        self._property_changed('long_rates_contribution')
        self.__long_rates_contribution = value        

    @property
    def importance(self) -> float:
        """Importance."""
        return self.__importance

    @importance.setter
    def importance(self, value: float):
        self._property_changed('importance')
        self.__importance = value        

    @property
    def source_date_span(self) -> float:
        """Date span for event in days."""
        return self.__source_date_span

    @source_date_span.setter
    def source_date_span(self, value: float):
        self._property_changed('source_date_span')
        self.__source_date_span = value        

    @property
    def ann_yield6_month(self) -> float:
        """Calculates the total return for 6 months, representing past performance."""
        return self.__ann_yield6_month

    @ann_yield6_month.setter
    def ann_yield6_month(self, value: float):
        self._property_changed('ann_yield6_month')
        self.__ann_yield6_month = value        

    @property
    def underlying_data_set_id(self) -> str:
        """Dataset on which this (virtual) dataset is based."""
        return self.__underlying_data_set_id

    @underlying_data_set_id.setter
    def underlying_data_set_id(self, value: str):
        self._property_changed('underlying_data_set_id')
        self.__underlying_data_set_id = value        

    @property
    def close_unadjusted(self) -> float:
        """Unadjusted Close level of an asset based on official exchange fixing or
           calculation agent marked level."""
        return self.__close_unadjusted

    @close_unadjusted.setter
    def close_unadjusted(self, value: float):
        self._property_changed('close_unadjusted')
        self.__close_unadjusted = value        

    @property
    def value_unit(self) -> str:
        """Value unit."""
        return self.__value_unit

    @value_unit.setter
    def value_unit(self, value: str):
        self._property_changed('value_unit')
        self.__value_unit = value        

    @property
    def quantity_unit(self) -> str:
        """Unit of measure for trade quantity."""
        return self.__quantity_unit

    @quantity_unit.setter
    def quantity_unit(self, value: str):
        self._property_changed('quantity_unit')
        self.__quantity_unit = value        

    @property
    def adjusted_low_price(self) -> float:
        """Adjusted low level of an asset based on official exchange fixing or calculation
           agent marked level."""
        return self.__adjusted_low_price

    @adjusted_low_price.setter
    def adjusted_low_price(self, value: float):
        self._property_changed('adjusted_low_price')
        self.__adjusted_low_price = value        

    @property
    def net_exposure_classification(self) -> str:
        """Classification for net exposure of fund."""
        return self.__net_exposure_classification

    @net_exposure_classification.setter
    def net_exposure_classification(self, value: str):
        self._property_changed('net_exposure_classification')
        self.__net_exposure_classification = value        

    @property
    def settlement_method(self) -> str:
        """Settlement method of the swap."""
        return self.__settlement_method

    @settlement_method.setter
    def settlement_method(self, value: str):
        self._property_changed('settlement_method')
        self.__settlement_method = value        

    @property
    def long_conviction_large(self) -> float:
        """The count of long ideas with large conviction."""
        return self.__long_conviction_large

    @long_conviction_large.setter
    def long_conviction_large(self, value: float):
        self._property_changed('long_conviction_large')
        self.__long_conviction_large = value        

    @property
    def alpha(self) -> float:
        """Alpha."""
        return self.__alpha

    @alpha.setter
    def alpha(self, value: float):
        self._property_changed('alpha')
        self.__alpha = value        

    @property
    def company(self) -> str:
        """Activity user company."""
        return self.__company

    @company.setter
    def company(self, value: str):
        self._property_changed('company')
        self.__company = value        

    @property
    def conviction_list(self) -> bool:
        """Conviction List, which is true if the security is on the Conviction Buy List or
           false otherwise. Securities with a convictionList value equal to true
           are by definition a subset of the securities with a rating equal to
           Buy."""
        return self.__conviction_list

    @conviction_list.setter
    def conviction_list(self, value: bool):
        self._property_changed('conviction_list')
        self.__conviction_list = value        

    @property
    def settlement_frequency(self) -> str:
        """Settlement Frequency provided by Participant (e.g., Monthly, Daily)."""
        return self.__settlement_frequency

    @settlement_frequency.setter
    def settlement_frequency(self, value: str):
        self._property_changed('settlement_frequency')
        self.__settlement_frequency = value        

    @property
    def dist_avg7_day(self) -> float:
        """Goldman custom calculated value, only used for GS onshore Money Market Funds,
           assumes sum of the past 7 days divided by 7 and expressed as a
           percent."""
        return self.__dist_avg7_day

    @dist_avg7_day.setter
    def dist_avg7_day(self, value: float):
        self._property_changed('dist_avg7_day')
        self.__dist_avg7_day = value        

    @property
    def remove_tape_c(self) -> float:
        """Goldman's rate for liquidity removing trades on tape C."""
        return self.__remove_tape_c

    @remove_tape_c.setter
    def remove_tape_c(self, value: float):
        self._property_changed('remove_tape_c')
        self.__remove_tape_c = value        

    @property
    def remove_tape_b(self) -> float:
        """Goldman's rate for liquidity removing trades on tape B."""
        return self.__remove_tape_b

    @remove_tape_b.setter
    def remove_tape_b(self, value: float):
        self._property_changed('remove_tape_b')
        self.__remove_tape_b = value        

    @property
    def in_risk_model(self) -> bool:
        """Whether or not the asset is in the risk model universe."""
        return self.__in_risk_model

    @in_risk_model.setter
    def in_risk_model(self, value: bool):
        self._property_changed('in_risk_model')
        self.__in_risk_model = value        

    @property
    def daily_net_shareholder_flows_percent(self) -> float:
        """Percent of assets paid daily."""
        return self.__daily_net_shareholder_flows_percent

    @daily_net_shareholder_flows_percent.setter
    def daily_net_shareholder_flows_percent(self, value: float):
        self._property_changed('daily_net_shareholder_flows_percent')
        self.__daily_net_shareholder_flows_percent = value        

    @property
    def type_of_return(self) -> str:
        """The type of return for the commodity index. Only applicable for commodity
           indices."""
        return self.__type_of_return

    @type_of_return.setter
    def type_of_return(self, value: str):
        self._property_changed('type_of_return')
        self.__type_of_return = value        

    @property
    def servicing_cost_long_pnl(self) -> float:
        """Servicing Cost Long Profit and Loss."""
        return self.__servicing_cost_long_pnl

    @servicing_cost_long_pnl.setter
    def servicing_cost_long_pnl(self, value: float):
        self._property_changed('servicing_cost_long_pnl')
        self.__servicing_cost_long_pnl = value        

    @property
    def excess_margin_percentage(self) -> float:
        """Available credit percentage."""
        return self.__excess_margin_percentage

    @excess_margin_percentage.setter
    def excess_margin_percentage(self, value: float):
        self._property_changed('excess_margin_percentage')
        self.__excess_margin_percentage = value        

    @property
    def remove_tape_a(self) -> float:
        """Goldman's rate for liquidity removing trades on tape A."""
        return self.__remove_tape_a

    @remove_tape_a.setter
    def remove_tape_a(self, value: float):
        self._property_changed('remove_tape_a')
        self.__remove_tape_a = value        

    @property
    def meeting_number(self) -> float:
        """Central bank meeting number."""
        return self.__meeting_number

    @meeting_number.setter
    def meeting_number(self, value: float):
        self._property_changed('meeting_number')
        self.__meeting_number = value        

    @property
    def exchange_id(self) -> str:
        """Unique identifier for an exchange."""
        return self.__exchange_id

    @exchange_id.setter
    def exchange_id(self, value: str):
        self._property_changed('exchange_id')
        self.__exchange_id = value        

    @property
    def mid_gspread(self) -> float:
        """Mid G spread."""
        return self.__mid_gspread

    @mid_gspread.setter
    def mid_gspread(self, value: float):
        self._property_changed('mid_gspread')
        self.__mid_gspread = value        

    @property
    def tcm_cost_horizon20_day(self) -> float:
        """TCM cost with a 20 day time horizon."""
        return self.__tcm_cost_horizon20_day

    @tcm_cost_horizon20_day.setter
    def tcm_cost_horizon20_day(self, value: float):
        self._property_changed('tcm_cost_horizon20_day')
        self.__tcm_cost_horizon20_day = value        

    @property
    def long_level(self) -> float:
        """Level of the 5-day normalized flow for long selling/buying."""
        return self.__long_level

    @long_level.setter
    def long_level(self, value: float):
        self._property_changed('long_level')
        self.__long_level = value        

    @property
    def realm(self) -> str:
        """Realm."""
        return self.__realm

    @realm.setter
    def realm(self, value: str):
        self._property_changed('realm')
        self.__realm = value        

    @property
    def bid(self) -> float:
        """Latest Bid Price (price willing to buy)."""
        return self.__bid

    @bid.setter
    def bid(self, value: float):
        self._property_changed('bid')
        self.__bid = value        

    @property
    def is_aggressive(self) -> float:
        """Indicates if the fill was aggressive or passive."""
        return self.__is_aggressive

    @is_aggressive.setter
    def is_aggressive(self, value: float):
        self._property_changed('is_aggressive')
        self.__is_aggressive = value        

    @property
    def order_id(self) -> str:
        """The unique ID of the order."""
        return self.__order_id

    @order_id.setter
    def order_id(self, value: str):
        self._property_changed('order_id')
        self.__order_id = value        

    @property
    def repo_rate(self) -> float:
        """Repurchase Rate."""
        return self.__repo_rate

    @repo_rate.setter
    def repo_rate(self, value: float):
        self._property_changed('repo_rate')
        self.__repo_rate = value        

    @property
    def market_cap_usd(self) -> float:
        """Market capitalization of a given asset denominated in USD."""
        return self.__market_cap_usd

    @market_cap_usd.setter
    def market_cap_usd(self, value: float):
        self._property_changed('market_cap_usd')
        self.__market_cap_usd = value        

    @property
    def high_price(self) -> float:
        """High level of an asset based on official exchange fixing or calculation agent
           marked level."""
        return self.__high_price

    @high_price.setter
    def high_price(self, value: float):
        self._property_changed('high_price')
        self.__high_price = value        

    @property
    def absolute_shares(self) -> float:
        """The number of shares without adjusting for side."""
        return self.__absolute_shares

    @absolute_shares.setter
    def absolute_shares(self, value: float):
        self._property_changed('absolute_shares')
        self.__absolute_shares = value        

    @property
    def action(self) -> str:
        """The activity action. For example: Viewed"""
        return self.__action

    @action.setter
    def action(self, value: str):
        self._property_changed('action')
        self.__action = value        

    @property
    def model(self) -> str:
        """Model."""
        return self.__model

    @model.setter
    def model(self, value: str):
        self._property_changed('model')
        self.__model = value        

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def arrival_haircut_vwap_normalized(self) -> float:
        """Performance against Benchmark in pip."""
        return self.__arrival_haircut_vwap_normalized

    @arrival_haircut_vwap_normalized.setter
    def arrival_haircut_vwap_normalized(self, value: float):
        self._property_changed('arrival_haircut_vwap_normalized')
        self.__arrival_haircut_vwap_normalized = value        

    @property
    def price_component(self) -> str:
        """Component of total price."""
        return self.__price_component

    @price_component.setter
    def price_component(self, value: str):
        self._property_changed('price_component')
        self.__price_component = value        

    @property
    def queue_clock_time_description(self) -> str:
        """Description of the Stock's Queue Clock Time on the particular date."""
        return self.__queue_clock_time_description

    @queue_clock_time_description.setter
    def queue_clock_time_description(self, value: str):
        self._property_changed('queue_clock_time_description')
        self.__queue_clock_time_description = value        

    @property
    def delta_strike(self) -> str:
        """Option strike price expressed in terms of delta * 100."""
        return self.__delta_strike

    @delta_strike.setter
    def delta_strike(self, value: str):
        self._property_changed('delta_strike')
        self.__delta_strike = value        

    @property
    def asset_parameters_notional_currency(self) -> str:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__asset_parameters_notional_currency

    @asset_parameters_notional_currency.setter
    def asset_parameters_notional_currency(self, value: str):
        self._property_changed('asset_parameters_notional_currency')
        self.__asset_parameters_notional_currency = value        

    @property
    def value_actual(self) -> str:
        """Latest released value."""
        return self.__value_actual

    @value_actual.setter
    def value_actual(self, value: str):
        self._property_changed('value_actual')
        self.__value_actual = value        

    @property
    def upi(self) -> str:
        """Unique product identifier for product."""
        return self.__upi

    @upi.setter
    def upi(self, value: str):
        self._property_changed('upi')
        self.__upi = value        

    @property
    def asset_types(self) -> Tuple[Tuple[Union[AssetType, str], ...], ...]:
        """Asset Types supported."""
        return self.__asset_types

    @asset_types.setter
    def asset_types(self, value: Tuple[Tuple[Union[AssetType, str], ...], ...]):
        self._property_changed('asset_types')
        self.__asset_types = value        

    @property
    def bcid(self) -> str:
        """Bloomberg composite identifier (ticker and country code)."""
        return self.__bcid

    @bcid.setter
    def bcid(self, value: str):
        self._property_changed('bcid')
        self.__bcid = value        

    @property
    def mkt_point(self) -> Tuple[str, ...]:
        """The MDAPI Point (e.g. 3m, 10y, 11y, Dec19)."""
        return self.__mkt_point

    @mkt_point.setter
    def mkt_point(self, value: Tuple[str, ...]):
        self._property_changed('mkt_point')
        self.__mkt_point = value        

    @property
    def collateral_currency(self) -> str:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__collateral_currency

    @collateral_currency.setter
    def collateral_currency(self, value: str):
        self._property_changed('collateral_currency')
        self.__collateral_currency = value        

    @property
    def restriction_start_date(self) -> datetime.date:
        """The date at which the security restriction was enacted."""
        return self.__restriction_start_date

    @restriction_start_date.setter
    def restriction_start_date(self, value: datetime.date):
        self._property_changed('restriction_start_date')
        self.__restriction_start_date = value        

    @property
    def original_country(self) -> str:
        """Country in source dataset."""
        return self.__original_country

    @original_country.setter
    def original_country(self, value: str):
        self._property_changed('original_country')
        self.__original_country = value        

    @property
    def touch_liquidity_score(self) -> float:
        """Z-score of the amount available to trade at the top of the aggregated order
           book."""
        return self.__touch_liquidity_score

    @touch_liquidity_score.setter
    def touch_liquidity_score(self, value: float):
        self._property_changed('touch_liquidity_score')
        self.__touch_liquidity_score = value        

    @property
    def field(self) -> str:
        """The market data field (e.g. rate, price). This can be resolved into a dataset
           when combined with vendor and intraday=true/false."""
        return self.__field

    @field.setter
    def field(self, value: str):
        self._property_changed('field')
        self.__field = value        

    @property
    def factor_category_id(self) -> str:
        """Id for Factor Categories."""
        return self.__factor_category_id

    @factor_category_id.setter
    def factor_category_id(self, value: str):
        self._property_changed('factor_category_id')
        self.__factor_category_id = value        

    @property
    def expected_completion_date(self) -> str:
        """Expected day of acquisition completion."""
        return self.__expected_completion_date

    @expected_completion_date.setter
    def expected_completion_date(self, value: str):
        self._property_changed('expected_completion_date')
        self.__expected_completion_date = value        

    @property
    def spread_option_vol(self) -> float:
        """Historical implied normal volatility for a liquid point on spread option vol
           surface."""
        return self.__spread_option_vol

    @spread_option_vol.setter
    def spread_option_vol(self, value: float):
        self._property_changed('spread_option_vol')
        self.__spread_option_vol = value        

    @property
    def inflation_swap_rate(self) -> float:
        """Zero coupon inflation swap break-even rate for a given currency."""
        return self.__inflation_swap_rate

    @inflation_swap_rate.setter
    def inflation_swap_rate(self, value: float):
        self._property_changed('inflation_swap_rate')
        self.__inflation_swap_rate = value        

    @property
    def fx_risk_premium_index(self) -> float:
        """FX risk premium index: percentage difference between average spot rate and OECD
           PPP exchange rate."""
        return self.__fx_risk_premium_index

    @fx_risk_premium_index.setter
    def fx_risk_premium_index(self, value: float):
        self._property_changed('fx_risk_premium_index')
        self.__fx_risk_premium_index = value        

    @property
    def skew(self) -> float:
        """Volatility skew."""
        return self.__skew

    @skew.setter
    def skew(self, value: float):
        self._property_changed('skew')
        self.__skew = value        

    @property
    def status(self) -> str:
        """Status of report run"""
        return self.__status

    @status.setter
    def status(self, value: str):
        self._property_changed('status')
        self.__status = value        

    @property
    def sustain_emerging_markets(self) -> bool:
        """True if the stock is on the SUSTAIN Emerging Markets list as of the
           corresponding date. False if the stock is removed from the SUSTAIN
           Emerging Markets list on the corresponding date."""
        return self.__sustain_emerging_markets

    @sustain_emerging_markets.setter
    def sustain_emerging_markets(self, value: bool):
        self._property_changed('sustain_emerging_markets')
        self.__sustain_emerging_markets = value        

    @property
    def event_date_time(self) -> datetime.datetime:
        """The time of the event if the event has a specific time, using UTC convention, or
           the end time of the event if the event occurs during a time window
           (optional)."""
        return self.__event_date_time

    @event_date_time.setter
    def event_date_time(self, value: datetime.datetime):
        self._property_changed('event_date_time')
        self.__event_date_time = value        

    @property
    def total_price(self) -> float:
        """Net price of the asset."""
        return self.__total_price

    @total_price.setter
    def total_price(self, value: float):
        self._property_changed('total_price')
        self.__total_price = value        

    @property
    def embeded_option(self) -> str:
        """An indication of whether or not the option fields are for an embedded option."""
        return self.__embeded_option

    @embeded_option.setter
    def embeded_option(self, value: str):
        self._property_changed('embeded_option')
        self.__embeded_option = value        

    @property
    def event_source(self) -> str:
        """Equals GS if the event is sourced from Goldman Sachs Global Investment Research
           analysts. Equals TR if the event is sourced from Refinitive
           StreetEvents."""
        return self.__event_source

    @event_source.setter
    def event_source(self, value: str):
        self._property_changed('event_source')
        self.__event_source = value        

    @property
    def on_behalf_of(self) -> str:
        """Marquee unique identifier"""
        return self.__on_behalf_of

    @on_behalf_of.setter
    def on_behalf_of(self, value: str):
        self._property_changed('on_behalf_of')
        self.__on_behalf_of = value        

    @property
    def qis_perm_no(self) -> str:
        """QIS Permanent Security Number."""
        return self.__qis_perm_no

    @qis_perm_no.setter
    def qis_perm_no(self, value: str):
        self._property_changed('qis_perm_no')
        self.__qis_perm_no = value        

    @property
    def shareclass_id(self) -> str:
        """Identifies shareclass with a unique code."""
        return self.__shareclass_id

    @shareclass_id.setter
    def shareclass_id(self, value: str):
        self._property_changed('shareclass_id')
        self.__shareclass_id = value        

    @property
    def exception_status(self) -> str:
        """The violation status for this particular line item."""
        return self.__exception_status

    @exception_status.setter
    def exception_status(self, value: str):
        self._property_changed('exception_status')
        self.__exception_status = value        

    @property
    def short_exposure(self) -> float:
        """Exposure of a given portfolio to securities which are short in direction. If you
           are $60 short and $40 long, shortExposure would be $60."""
        return self.__short_exposure

    @short_exposure.setter
    def short_exposure(self, value: float):
        self._property_changed('short_exposure')
        self.__short_exposure = value        

    @property
    def tcm_cost_participation_rate10_pct(self) -> float:
        """TCM cost with a 10 percent participation rate."""
        return self.__tcm_cost_participation_rate10_pct

    @tcm_cost_participation_rate10_pct.setter
    def tcm_cost_participation_rate10_pct(self, value: float):
        self._property_changed('tcm_cost_participation_rate10_pct')
        self.__tcm_cost_participation_rate10_pct = value        

    @property
    def event_time(self) -> str:
        """The time of the event if the event has a specific time or the end time of the
           event if the event occurs during a time window (optional). It is
           represented in HH:MM 24 hour format in the time zone of the exchange
           where the company is listed."""
        return self.__event_time

    @event_time.setter
    def event_time(self, value: str):
        self._property_changed('event_time')
        self.__event_time = value        

    @property
    def delivery_date(self) -> datetime.date:
        """The final date by which the underlying commodity for a futures contract must be
           delivered in order for the terms of the contract to be fulfilled."""
        return self.__delivery_date

    @delivery_date.setter
    def delivery_date(self, value: datetime.date):
        self._property_changed('delivery_date')
        self.__delivery_date = value        

    @property
    def arrival_haircut_vwap(self) -> float:
        """Arrival Haircut VWAP."""
        return self.__arrival_haircut_vwap

    @arrival_haircut_vwap.setter
    def arrival_haircut_vwap(self, value: float):
        self._property_changed('arrival_haircut_vwap')
        self.__arrival_haircut_vwap = value        

    @property
    def interest_rate(self) -> float:
        """Interest rate."""
        return self.__interest_rate

    @interest_rate.setter
    def interest_rate(self, value: float):
        self._property_changed('interest_rate')
        self.__interest_rate = value        

    @property
    def execution_days(self) -> float:
        """Number of days to used to execute."""
        return self.__execution_days

    @execution_days.setter
    def execution_days(self, value: float):
        self._property_changed('execution_days')
        self.__execution_days = value        

    @property
    def recall_due_date(self) -> datetime.date:
        """Date in which the recall of securities in a stock loan recall activity must be
           complete."""
        return self.__recall_due_date

    @recall_due_date.setter
    def recall_due_date(self, value: datetime.date):
        self._property_changed('recall_due_date')
        self.__recall_due_date = value        

    @property
    def side(self) -> str:
        """Long or short."""
        return self.__side

    @side.setter
    def side(self, value: str):
        self._property_changed('side')
        self.__side = value        

    @property
    def forward(self) -> float:
        """Forward value."""
        return self.__forward

    @forward.setter
    def forward(self, value: float):
        self._property_changed('forward')
        self.__forward = value        

    @property
    def borrow_fee(self) -> float:
        """An indication of the rate one would be charged for borrowing/shorting the
           relevant asset on that day, expressed in annualized percent terms.
           Rates may change daily."""
        return self.__borrow_fee

    @borrow_fee.setter
    def borrow_fee(self, value: float):
        self._property_changed('borrow_fee')
        self.__borrow_fee = value        

    @property
    def update_time(self) -> datetime.datetime:
        """Update time of the data element, which allows historical as-of query."""
        return self.__update_time

    @update_time.setter
    def update_time(self, value: datetime.datetime):
        self._property_changed('update_time')
        self.__update_time = value        

    @property
    def loan_spread(self) -> float:
        """The difference between the investment rate on cash collateral and the rebate
           rate of a loan."""
        return self.__loan_spread

    @loan_spread.setter
    def loan_spread(self, value: float):
        self._property_changed('loan_spread')
        self.__loan_spread = value        

    @property
    def tcm_cost_horizon12_hour(self) -> float:
        """TCM cost with a 12 hour time horizon."""
        return self.__tcm_cost_horizon12_hour

    @tcm_cost_horizon12_hour.setter
    def tcm_cost_horizon12_hour(self, value: float):
        self._property_changed('tcm_cost_horizon12_hour')
        self.__tcm_cost_horizon12_hour = value        

    @property
    def dew_point(self) -> float:
        """Temperature in fahrenheit below which water condenses."""
        return self.__dew_point

    @dew_point.setter
    def dew_point(self, value: float):
        self._property_changed('dew_point')
        self.__dew_point = value        

    @property
    def research_commission(self) -> float:
        """The dollar amount of commissions received from clients."""
        return self.__research_commission

    @research_commission.setter
    def research_commission(self, value: float):
        self._property_changed('research_commission')
        self.__research_commission = value        

    @property
    def leg_one_delivery_point(self) -> str:
        """Delivery point of leg."""
        return self.__leg_one_delivery_point

    @leg_one_delivery_point.setter
    def leg_one_delivery_point(self, value: str):
        self._property_changed('leg_one_delivery_point')
        self.__leg_one_delivery_point = value        

    @property
    def event_status(self) -> str:
        """Included if there is additional information about an event, such as the event
           being cancelled."""
        return self.__event_status

    @event_status.setter
    def event_status(self, value: str):
        self._property_changed('event_status')
        self.__event_status = value        

    @property
    def sell_date(self) -> datetime.date:
        """Sell date of the securities triggering the stock loan recall activity."""
        return self.__sell_date

    @sell_date.setter
    def sell_date(self, value: datetime.date):
        self._property_changed('sell_date')
        self.__sell_date = value        

    @property
    def asset_parameters_settlement(self) -> str:
        """Settlement type."""
        return self.__asset_parameters_settlement

    @asset_parameters_settlement.setter
    def asset_parameters_settlement(self, value: str):
        self._property_changed('asset_parameters_settlement')
        self.__asset_parameters_settlement = value        

    @property
    def return_(self) -> float:
        """Return of asset over a given period (e.g. close-to-close)."""
        return self.__return

    @return_.setter
    def return_(self, value: float):
        self._property_changed('return_')
        self.__return = value        

    @property
    def max_temperature(self) -> float:
        """Maximum temperature observed on a given day in fahrenheit."""
        return self.__max_temperature

    @max_temperature.setter
    def max_temperature(self, value: float):
        self._property_changed('max_temperature')
        self.__max_temperature = value        

    @property
    def acquirer_shareholder_meeting_date(self) -> str:
        """Shareholders meeting date for acquiring entity."""
        return self.__acquirer_shareholder_meeting_date

    @acquirer_shareholder_meeting_date.setter
    def acquirer_shareholder_meeting_date(self, value: str):
        self._property_changed('acquirer_shareholder_meeting_date')
        self.__acquirer_shareholder_meeting_date = value        

    @property
    def notional_amount(self) -> float:
        """Only applicable on Commodity Index products."""
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: float):
        self._property_changed('notional_amount')
        self.__notional_amount = value        

    @property
    def pay_or_receive(self) -> str:
        """Pay or receive fixed"""
        return self.__pay_or_receive

    @pay_or_receive.setter
    def pay_or_receive(self, value: str):
        self._property_changed('pay_or_receive')
        self.__pay_or_receive = value        

    @property
    def arrival_rt_normalized(self) -> float:
        """Performance against Benchmark in pip."""
        return self.__arrival_rt_normalized

    @arrival_rt_normalized.setter
    def arrival_rt_normalized(self, value: float):
        self._property_changed('arrival_rt_normalized')
        self.__arrival_rt_normalized = value        

    @property
    def report_type(self) -> str:
        """Type of report to execute"""
        return self.__report_type

    @report_type.setter
    def report_type(self, value: str):
        self._property_changed('report_type')
        self.__report_type = value        

    @property
    def source_url(self) -> str:
        """Source URL."""
        return self.__source_url

    @source_url.setter
    def source_url(self, value: str):
        self._property_changed('source_url')
        self.__source_url = value        

    @property
    def estimated_return(self) -> float:
        """Estimated return of asset over a given period (e.g. close-to-close)."""
        return self.__estimated_return

    @estimated_return.setter
    def estimated_return(self, value: float):
        self._property_changed('estimated_return')
        self.__estimated_return = value        

    @property
    def high(self) -> float:
        """High level of an asset based on official exchange fixing or calculation agent
           marked level."""
        return self.__high

    @high.setter
    def high(self, value: float):
        self._property_changed('high')
        self.__high = value        

    @property
    def source_last_update(self) -> str:
        """Source last update."""
        return self.__source_last_update

    @source_last_update.setter
    def source_last_update(self, value: str):
        self._property_changed('source_last_update')
        self.__source_last_update = value        

    @property
    def quantity_mw(self) -> float:
        """Quantity of electricity in megawatts."""
        return self.__quantity_mw

    @quantity_mw.setter
    def quantity_mw(self, value: float):
        self._property_changed('quantity_mw')
        self.__quantity_mw = value        

    @property
    def pnode_id(self) -> str:
        """Pricing node identifier sourced from Morningstar."""
        return self.__pnode_id

    @pnode_id.setter
    def pnode_id(self, value: str):
        self._property_changed('pnode_id')
        self.__pnode_id = value        

    @property
    def event_name(self) -> str:
        """Event name."""
        return self.__event_name

    @event_name.setter
    def event_name(self, value: str):
        self._property_changed('event_name')
        self.__event_name = value        

    @property
    def indication_of_other_price_affecting_term(self) -> str:
        """An indication that the publicly reportable SB swap transaction has one or more
           additional term(s) or provision(s), other than those listed in the
           required real-time data fields, that materially affect(s) the price
           of the swap transaction."""
        return self.__indication_of_other_price_affecting_term

    @indication_of_other_price_affecting_term.setter
    def indication_of_other_price_affecting_term(self, value: str):
        self._property_changed('indication_of_other_price_affecting_term')
        self.__indication_of_other_price_affecting_term = value        

    @property
    def unadjusted_bid(self) -> float:
        """Unadjusted bid level of an asset based on official exchange fixing or
           calculation agent marked level."""
        return self.__unadjusted_bid

    @unadjusted_bid.setter
    def unadjusted_bid(self, value: float):
        self._property_changed('unadjusted_bid')
        self.__unadjusted_bid = value        

    @property
    def backtest_type(self) -> str:
        """Backtest type differentiates the backtest type."""
        return self.__backtest_type

    @backtest_type.setter
    def backtest_type(self, value: str):
        self._property_changed('backtest_type')
        self.__backtest_type = value        

    @property
    def gsdeer(self) -> float:
        """Goldman Sachs Dynamic Equilibrium Exchange Rate."""
        return self.__gsdeer

    @gsdeer.setter
    def gsdeer(self, value: float):
        self._property_changed('gsdeer')
        self.__gsdeer = value        

    @property
    def g_regional_percentile(self) -> float:
        """A percentile that captures a company???s G ranking relative to its region."""
        return self.__g_regional_percentile

    @g_regional_percentile.setter
    def g_regional_percentile(self, value: float):
        self._property_changed('g_regional_percentile')
        self.__g_regional_percentile = value        

    @property
    def prev_close_ask(self) -> float:
        """Previous business day's close ask price."""
        return self.__prev_close_ask

    @prev_close_ask.setter
    def prev_close_ask(self, value: float):
        self._property_changed('prev_close_ask')
        self.__prev_close_ask = value        

    @property
    def level(self) -> float:
        """Level of the 5-day normalized flow in a given factor."""
        return self.__level

    @level.setter
    def level(self, value: float):
        self._property_changed('level')
        self.__level = value        

    @property
    def mnav(self) -> float:
        """Net asset value, assets of a fund (ex dividend) divided by total number of
           shares."""
        return self.__mnav

    @mnav.setter
    def mnav(self, value: float):
        self._property_changed('mnav')
        self.__mnav = value        

    @property
    def es_momentum_score(self) -> float:
        """A company???s score for E&S momentum."""
        return self.__es_momentum_score

    @es_momentum_score.setter
    def es_momentum_score(self, value: float):
        self._property_changed('es_momentum_score')
        self.__es_momentum_score = value        

    @property
    def curr_yield7_day(self) -> float:
        """Average income return over previous 7 days reduced by any capital gains that may
           have been included in rate calculation, according to the current
           amount."""
        return self.__curr_yield7_day

    @curr_yield7_day.setter
    def curr_yield7_day(self, value: float):
        self._property_changed('curr_yield7_day')
        self.__curr_yield7_day = value        

    @property
    def pressure(self) -> float:
        """Average barometric pressure on a given day in inches of mercury."""
        return self.__pressure

    @pressure.setter
    def pressure(self, value: float):
        self._property_changed('pressure')
        self.__pressure = value        

    @property
    def short_description(self) -> str:
        """Short description of dataset."""
        return self.__short_description

    @short_description.setter
    def short_description(self, value: str):
        self._property_changed('short_description')
        self.__short_description = value        

    @property
    def feed(self) -> str:
        """Indicates the source feed of the data."""
        return self.__feed

    @feed.setter
    def feed(self, value: str):
        self._property_changed('feed')
        self.__feed = value        

    @property
    def net_weight(self) -> float:
        """Difference between the longWeight and shortWeight. If you have IBM stock with
           shortWeight 0.2 and also IBM stock with longWeight 0.4, then the
           netWeight would be 0.2 (-0.2+0.4)."""
        return self.__net_weight

    @net_weight.setter
    def net_weight(self, value: float):
        self._property_changed('net_weight')
        self.__net_weight = value        

    @property
    def portfolio_managers(self) -> Tuple[str, ...]:
        """Portfolio managers of asset."""
        return self.__portfolio_managers

    @portfolio_managers.setter
    def portfolio_managers(self, value: Tuple[str, ...]):
        self._property_changed('portfolio_managers')
        self.__portfolio_managers = value        

    @property
    def asset_parameters_commodity_sector(self) -> str:
        """The sector of the commodity"""
        return self.__asset_parameters_commodity_sector

    @asset_parameters_commodity_sector.setter
    def asset_parameters_commodity_sector(self, value: str):
        self._property_changed('asset_parameters_commodity_sector')
        self.__asset_parameters_commodity_sector = value        

    @property
    def bos_in_ticks(self) -> float:
        """The Bid-Offer Spread of the stock in Ticks on the particular date."""
        return self.__bos_in_ticks

    @bos_in_ticks.setter
    def bos_in_ticks(self, value: float):
        self._property_changed('bos_in_ticks')
        self.__bos_in_ticks = value        

    @property
    def price_notation2(self) -> float:
        """The Basis points, Price, Yield, Spread, Coupon, etc., value depending on the
           type of SB swap, which is calculated at affirmation."""
        return self.__price_notation2

    @price_notation2.setter
    def price_notation2(self, value: float):
        self._property_changed('price_notation2')
        self.__price_notation2 = value        

    @property
    def market_buffer_threshold(self) -> float:
        """The required buffer between holdings and on loan quantity for a market."""
        return self.__market_buffer_threshold

    @market_buffer_threshold.setter
    def market_buffer_threshold(self, value: float):
        self._property_changed('market_buffer_threshold')
        self.__market_buffer_threshold = value        

    @property
    def price_notation3(self) -> float:
        """The Basis points, Price, Yield, Spread, Coupon, etc., value depending on the
           type of SB swap, which is calculated at affirmation."""
        return self.__price_notation3

    @price_notation3.setter
    def price_notation3(self, value: float):
        self._property_changed('price_notation3')
        self.__price_notation3 = value        

    @property
    def cap_floor_vol(self) -> float:
        """Historical implied normal volatility for a liquid point on cap and floor vol
           surface."""
        return self.__cap_floor_vol

    @cap_floor_vol.setter
    def cap_floor_vol(self, value: float):
        self._property_changed('cap_floor_vol')
        self.__cap_floor_vol = value        

    @property
    def notional(self) -> float:
        """Notional."""
        return self.__notional

    @notional.setter
    def notional(self, value: float):
        self._property_changed('notional')
        self.__notional = value        

    @property
    def es_disclosure_percentage(self) -> float:
        """Percentage of E&S metrics disclosed by the company."""
        return self.__es_disclosure_percentage

    @es_disclosure_percentage.setter
    def es_disclosure_percentage(self, value: float):
        self._property_changed('es_disclosure_percentage')
        self.__es_disclosure_percentage = value        

    @property
    def investment_income(self) -> float:
        """The income earned by the reinvested collateral."""
        return self.__investment_income

    @investment_income.setter
    def investment_income(self, value: float):
        self._property_changed('investment_income')
        self.__investment_income = value        

    @property
    def client_short_name(self) -> str:
        """The short name of a client."""
        return self.__client_short_name

    @client_short_name.setter
    def client_short_name(self, value: str):
        self._property_changed('client_short_name')
        self.__client_short_name = value        

    @property
    def bid_plus_ask(self) -> float:
        """Sum of bid & ask."""
        return self.__bid_plus_ask

    @bid_plus_ask.setter
    def bid_plus_ask(self, value: float):
        self._property_changed('bid_plus_ask')
        self.__bid_plus_ask = value        

    @property
    def foreign_ccy_rate(self) -> float:
        """The interest rate of the foreign currency of the associated FX contract."""
        return self.__foreign_ccy_rate

    @foreign_ccy_rate.setter
    def foreign_ccy_rate(self, value: float):
        self._property_changed('foreign_ccy_rate')
        self.__foreign_ccy_rate = value        

    @property
    def election_odds(self) -> float:
        """Odds of winning election."""
        return self.__election_odds

    @election_odds.setter
    def election_odds(self, value: float):
        self._property_changed('election_odds')
        self.__election_odds = value        

    @property
    def require_anon_client_name(self) -> bool:
        """Requires Anonymization of Client Name."""
        return self.__require_anon_client_name

    @require_anon_client_name.setter
    def require_anon_client_name(self, value: bool):
        self._property_changed('require_anon_client_name')
        self.__require_anon_client_name = value        

    @property
    def total(self) -> float:
        """Total exposure."""
        return self.__total

    @total.setter
    def total(self, value: float):
        self._property_changed('total')
        self.__total = value        

    @property
    def asset_id(self) -> str:
        """Marquee unique asset identifier."""
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: str):
        self._property_changed('asset_id')
        self.__asset_id = value        

    @property
    def mkt_type(self) -> str:
        """The MDAPI Type (e.g. IR_BASIS, FX_Vol)."""
        return self.__mkt_type

    @mkt_type.setter
    def mkt_type(self, value: str):
        self._property_changed('mkt_type')
        self.__mkt_type = value        

    @property
    def last_updated_time(self) -> datetime.datetime:
        """Timestamp of when the object was last updated"""
        return self.__last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, value: datetime.datetime):
        self._property_changed('last_updated_time')
        self.__last_updated_time = value        

    @property
    def pricing_location(self) -> str:
        """Quill pricing location."""
        return self.__pricing_location

    @pricing_location.setter
    def pricing_location(self, value: str):
        self._property_changed('pricing_location')
        self.__pricing_location = value        

    @property
    def yield30_day(self) -> float:
        """Net income per share for last 30 days/NAV."""
        return self.__yield30_day

    @yield30_day.setter
    def yield30_day(self, value: float):
        self._property_changed('yield30_day')
        self.__yield30_day = value        

    @property
    def proportion_of_risk(self) -> float:
        """Proportion of risk with respect to the portfolio's total risk."""
        return self.__proportion_of_risk

    @proportion_of_risk.setter
    def proportion_of_risk(self, value: float):
        self._property_changed('proportion_of_risk')
        self.__proportion_of_risk = value        

    @property
    def beta(self) -> float:
        """Beta."""
        return self.__beta

    @beta.setter
    def beta(self, value: float):
        self._property_changed('beta')
        self.__beta = value        

    @property
    def upfront_payment_date(self) -> datetime.date:
        """Date of upront payment."""
        return self.__upfront_payment_date

    @upfront_payment_date.setter
    def upfront_payment_date(self, value: datetime.date):
        self._property_changed('upfront_payment_date')
        self.__upfront_payment_date = value        

    @property
    def long_exposure(self) -> float:
        """Exposure of a given portfolio to securities which are long in direction. If you
           are $60 short and $40 long, longExposure would be $40."""
        return self.__long_exposure

    @long_exposure.setter
    def long_exposure(self, value: float):
        self._property_changed('long_exposure')
        self.__long_exposure = value        

    @property
    def tcm_cost_participation_rate20_pct(self) -> float:
        """TCM cost with a 20 percent participation rate."""
        return self.__tcm_cost_participation_rate20_pct

    @tcm_cost_participation_rate20_pct.setter
    def tcm_cost_participation_rate20_pct(self, value: float):
        self._property_changed('tcm_cost_participation_rate20_pct')
        self.__tcm_cost_participation_rate20_pct = value        

    @property
    def multi_asset_class_swap(self) -> str:
        """Indicates if the swap falls under multiple asset classes."""
        return self.__multi_asset_class_swap

    @multi_asset_class_swap.setter
    def multi_asset_class_swap(self, value: str):
        self._property_changed('multi_asset_class_swap')
        self.__multi_asset_class_swap = value        

    @property
    def idea_status(self) -> str:
        """The activity status of the idea."""
        return self.__idea_status

    @idea_status.setter
    def idea_status(self, value: str):
        self._property_changed('idea_status')
        self.__idea_status = value        

    @property
    def contract_subtype(self) -> str:
        """Contract subtype."""
        return self.__contract_subtype

    @contract_subtype.setter
    def contract_subtype(self, value: str):
        self._property_changed('contract_subtype')
        self.__contract_subtype = value        

    @property
    def fx_forecast(self) -> float:
        """FX forecast value for the relative period."""
        return self.__fx_forecast

    @fx_forecast.setter
    def fx_forecast(self, value: float):
        self._property_changed('fx_forecast')
        self.__fx_forecast = value        

    @property
    def fixing_time_label(self) -> str:
        """Time at which the fixing was taken."""
        return self.__fixing_time_label

    @fixing_time_label.setter
    def fixing_time_label(self, value: str):
        self._property_changed('fixing_time_label')
        self.__fixing_time_label = value        

    @property
    def implementation_id(self) -> str:
        """Marquee unique Implementation identifier."""
        return self.__implementation_id

    @implementation_id.setter
    def implementation_id(self, value: str):
        self._property_changed('implementation_id')
        self.__implementation_id = value        

    @property
    def fill_id(self) -> str:
        """Unique identifier for a fill."""
        return self.__fill_id

    @fill_id.setter
    def fill_id(self, value: str):
        self._property_changed('fill_id')
        self.__fill_id = value        

    @property
    def excess_returns(self) -> float:
        """Excess returns for backtest."""
        return self.__excess_returns

    @excess_returns.setter
    def excess_returns(self, value: float):
        self._property_changed('excess_returns')
        self.__excess_returns = value        

    @property
    def dollar_return(self) -> float:
        """Dollar return of asset over a given period (e.g. close-to-close)."""
        return self.__dollar_return

    @dollar_return.setter
    def dollar_return(self, value: float):
        self._property_changed('dollar_return')
        self.__dollar_return = value        

    @property
    def es_numeric_score(self) -> float:
        """Score for E&S numeric metrics."""
        return self.__es_numeric_score

    @es_numeric_score.setter
    def es_numeric_score(self, value: float):
        self._property_changed('es_numeric_score')
        self.__es_numeric_score = value        

    @property
    def in_benchmark(self) -> bool:
        """Whether or not the asset is in the benchmark."""
        return self.__in_benchmark

    @in_benchmark.setter
    def in_benchmark(self, value: bool):
        self._property_changed('in_benchmark')
        self.__in_benchmark = value        

    @property
    def return_on_equity(self) -> float:
        """Return on equity."""
        return self.__return_on_equity

    @return_on_equity.setter
    def return_on_equity(self, value: float):
        self._property_changed('return_on_equity')
        self.__return_on_equity = value        

    @property
    def action_sdr(self) -> str:
        """An indication that a publicly reportable securitybased (SB) swap transaction has
           been incorrectly or erroneously publicly disseminated and is canceled
           or corrected or a new transaction."""
        return self.__action_sdr

    @action_sdr.setter
    def action_sdr(self, value: str):
        self._property_changed('action_sdr')
        self.__action_sdr = value        

    @property
    def restriction_end_date(self) -> datetime.date:
        """The date at which the security restriction was lifted."""
        return self.__restriction_end_date

    @restriction_end_date.setter
    def restriction_end_date(self, value: datetime.date):
        self._property_changed('restriction_end_date')
        self.__restriction_end_date = value        

    @property
    def queue_in_lots_description(self) -> str:
        """Description of the Stock's Queue size in Lots (if applicable) on the particular
           date."""
        return self.__queue_in_lots_description

    @queue_in_lots_description.setter
    def queue_in_lots_description(self, value: str):
        self._property_changed('queue_in_lots_description')
        self.__queue_in_lots_description = value        

    @property
    def objective(self) -> str:
        """The objective of the hedge."""
        return self.__objective

    @objective.setter
    def objective(self, value: str):
        self._property_changed('objective')
        self.__objective = value        

    @property
    def nav_price(self) -> float:
        """Net asset value price. Quoted price (mid, 100 ??? Upfront) of the underlying
           basket of single name CDS. (Theoretical Index value). In percent."""
        return self.__nav_price

    @nav_price.setter
    def nav_price(self, value: float):
        self._property_changed('nav_price')
        self.__nav_price = value        

    @property
    def precipitation(self) -> float:
        """Amount of rainfall in inches."""
        return self.__precipitation

    @precipitation.setter
    def precipitation(self, value: float):
        self._property_changed('precipitation')
        self.__precipitation = value        

    @property
    def hedge_notional(self) -> float:
        """Notional value of the hedge."""
        return self.__hedge_notional

    @hedge_notional.setter
    def hedge_notional(self, value: float):
        self._property_changed('hedge_notional')
        self.__hedge_notional = value        

    @property
    def ask_low(self) -> float:
        """The lowest ask Price (price offering to sell)."""
        return self.__ask_low

    @ask_low.setter
    def ask_low(self, value: float):
        self._property_changed('ask_low')
        self.__ask_low = value        

    @property
    def beta_adjusted_net_exposure(self) -> float:
        """Beta adjusted net exposure."""
        return self.__beta_adjusted_net_exposure

    @beta_adjusted_net_exposure.setter
    def beta_adjusted_net_exposure(self, value: float):
        self._property_changed('beta_adjusted_net_exposure')
        self.__beta_adjusted_net_exposure = value        

    @property
    def avg_monthly_yield(self) -> float:
        """Only used for GS Money Market funds, assumes sum of the past 30 days, divided by
           30, and expressed as a percent."""
        return self.__avg_monthly_yield

    @avg_monthly_yield.setter
    def avg_monthly_yield(self, value: float):
        self._property_changed('avg_monthly_yield')
        self.__avg_monthly_yield = value        

    @property
    def period_direction(self) -> str:
        """Direction of the outlook period."""
        return self.__period_direction

    @period_direction.setter
    def period_direction(self, value: str):
        self._property_changed('period_direction')
        self.__period_direction = value        

    @property
    def earnings_per_share(self) -> float:
        """Earnings per share."""
        return self.__earnings_per_share

    @earnings_per_share.setter
    def earnings_per_share(self, value: float):
        self._property_changed('earnings_per_share')
        self.__earnings_per_share = value        

    @property
    def strike_percentage(self) -> float:
        """Strike compared to market value."""
        return self.__strike_percentage

    @strike_percentage.setter
    def strike_percentage(self, value: float):
        self._property_changed('strike_percentage')
        self.__strike_percentage = value        

    @property
    def excess_return_price(self) -> float:
        """The excess return price of an instrument."""
        return self.__excess_return_price

    @excess_return_price.setter
    def excess_return_price(self, value: float):
        self._property_changed('excess_return_price')
        self.__excess_return_price = value        

    @property
    def prev_close_bid(self) -> float:
        """Previous close BID price."""
        return self.__prev_close_bid

    @prev_close_bid.setter
    def prev_close_bid(self, value: float):
        self._property_changed('prev_close_bid')
        self.__prev_close_bid = value        

    @property
    def fx_pnl(self) -> float:
        """Foreign Exchange Profit and Loss (PNL)."""
        return self.__fx_pnl

    @fx_pnl.setter
    def fx_pnl(self, value: float):
        self._property_changed('fx_pnl')
        self.__fx_pnl = value        

    @property
    def tcm_cost_horizon16_day(self) -> float:
        """TCM cost with a 16 day time horizon."""
        return self.__tcm_cost_horizon16_day

    @tcm_cost_horizon16_day.setter
    def tcm_cost_horizon16_day(self, value: float):
        self._property_changed('tcm_cost_horizon16_day')
        self.__tcm_cost_horizon16_day = value        

    @property
    def settlement_date(self) -> datetime.date:
        """The settlement date of the associated FX contract."""
        return self.__settlement_date

    @settlement_date.setter
    def settlement_date(self, value: datetime.date):
        self._property_changed('settlement_date')
        self.__settlement_date = value        

    @property
    def sales_per_share(self) -> float:
        """Sales per share."""
        return self.__sales_per_share

    @sales_per_share.setter
    def sales_per_share(self, value: float):
        self._property_changed('sales_per_share')
        self.__sales_per_share = value        

    @property
    def unadjusted_close(self) -> float:
        """Unadjusted Close level of an asset based on official exchange fixing or
           calculation agent marked level."""
        return self.__unadjusted_close

    @unadjusted_close.setter
    def unadjusted_close(self, value: float):
        self._property_changed('unadjusted_close')
        self.__unadjusted_close = value        

    @property
    def loan_date(self) -> datetime.date:
        """The date at which the securities loan was enacted."""
        return self.__loan_date

    @loan_date.setter
    def loan_date(self, value: datetime.date):
        self._property_changed('loan_date')
        self.__loan_date = value        

    @property
    def lending_sec_id(self) -> str:
        """Securities lending identifiter for the security on loan."""
        return self.__lending_sec_id

    @lending_sec_id.setter
    def lending_sec_id(self, value: str):
        self._property_changed('lending_sec_id')
        self.__lending_sec_id = value        

    @property
    def equity_theta(self) -> float:
        """Theta exposure to equity products."""
        return self.__equity_theta

    @equity_theta.setter
    def equity_theta(self, value: float):
        self._property_changed('equity_theta')
        self.__equity_theta = value        

    @property
    def execution_fee(self) -> float:
        """Goldman's rate for all executions (e.g. dark pool fees, which charge the same
           fee for all trade types)."""
        return self.__execution_fee

    @execution_fee.setter
    def execution_fee(self, value: float):
        self._property_changed('execution_fee')
        self.__execution_fee = value        

    @property
    def start_date(self) -> datetime.date:
        """Start date specific to an asset. For example start date for the swap."""
        return self.__start_date

    @start_date.setter
    def start_date(self, value: datetime.date):
        self._property_changed('start_date')
        self.__start_date = value        

    @property
    def collateral_percentage_actual(self) -> float:
        """Collateral percentage covering contractual the given position."""
        return self.__collateral_percentage_actual

    @collateral_percentage_actual.setter
    def collateral_percentage_actual(self, value: float):
        self._property_changed('collateral_percentage_actual')
        self.__collateral_percentage_actual = value        

    @property
    def mixed_swap(self) -> str:
        """Indicates if the swap falls under both the CFTC and SEC jurisdictions."""
        return self.__mixed_swap

    @mixed_swap.setter
    def mixed_swap(self, value: str):
        self._property_changed('mixed_swap')
        self.__mixed_swap = value        

    @property
    def snowfall(self) -> float:
        """Amount of snowfall in inches."""
        return self.__snowfall

    @snowfall.setter
    def snowfall(self, value: float):
        self._property_changed('snowfall')
        self.__snowfall = value        

    @property
    def mic(self) -> str:
        """Market identifier code."""
        return self.__mic

    @mic.setter
    def mic(self, value: str):
        self._property_changed('mic')
        self.__mic = value        

    @property
    def mid(self) -> float:
        """Mid."""
        return self.__mid

    @mid.setter
    def mid(self, value: float):
        self._property_changed('mid')
        self.__mid = value        

    @property
    def relative_return_ytd(self) -> float:
        """Relative Return Year to Date."""
        return self.__relative_return_ytd

    @relative_return_ytd.setter
    def relative_return_ytd(self, value: float):
        self._property_changed('relative_return_ytd')
        self.__relative_return_ytd = value        

    @property
    def long(self) -> float:
        """Long exposure."""
        return self.__long

    @long.setter
    def long(self, value: float):
        self._property_changed('long')
        self.__long = value        

    @property
    def region_code(self) -> str:
        """ISO 3166 Region Code. Generally a three digit code."""
        return self.__region_code

    @region_code.setter
    def region_code(self, value: str):
        self._property_changed('region_code')
        self.__region_code = value        

    @property
    def long_weight(self) -> float:
        """Long weight of a position in a given portfolio. Equivalent to position long
           exposure / total long exposure. If you have a position with a
           longExposure of $20, and your portfolio longExposure is $100,
           longWeight would be 0.2 (20/100)."""
        return self.__long_weight

    @long_weight.setter
    def long_weight(self, value: float):
        self._property_changed('long_weight')
        self.__long_weight = value        

    @property
    def calculation_time(self) -> int:
        """Time taken to calculate risk metric (ms)."""
        return self.__calculation_time

    @calculation_time.setter
    def calculation_time(self, value: int):
        self._property_changed('calculation_time')
        self.__calculation_time = value        

    @property
    def average_realized_variance(self) -> float:
        """Average variance of an asset realized by observations of market prices."""
        return self.__average_realized_variance

    @average_realized_variance.setter
    def average_realized_variance(self, value: float):
        self._property_changed('average_realized_variance')
        self.__average_realized_variance = value        

    @property
    def financial_returns_score(self) -> float:
        """Financial Returns percentile relative to Americas coverage universe (a higher
           score means stronger financial returns)."""
        return self.__financial_returns_score

    @financial_returns_score.setter
    def financial_returns_score(self, value: float):
        self._property_changed('financial_returns_score')
        self.__financial_returns_score = value        

    @property
    def year_or_quarter(self) -> str:
        """Year or quarter for which the forecast holds."""
        return self.__year_or_quarter

    @year_or_quarter.setter
    def year_or_quarter(self, value: str):
        self._property_changed('year_or_quarter')
        self.__year_or_quarter = value        

    @property
    def settlement_type(self) -> str:
        """Swap Settlement Type"""
        return self.__settlement_type

    @settlement_type.setter
    def settlement_type(self, value: str):
        self._property_changed('settlement_type')
        self.__settlement_type = value        

    @property
    def net_change(self) -> float:
        """Difference between the lastest trading price or value and the adjusted
           historical closing value or settlement price."""
        return self.__net_change

    @net_change.setter
    def net_change(self, value: float):
        self._property_changed('net_change')
        self.__net_change = value        

    @property
    def non_symbol_dimensions(self) -> Tuple[str, ...]:
        """Fields that are not nullable."""
        return self.__non_symbol_dimensions

    @non_symbol_dimensions.setter
    def non_symbol_dimensions(self, value: Tuple[str, ...]):
        self._property_changed('non_symbol_dimensions')
        self.__non_symbol_dimensions = value        

    @property
    def leg_two_fixed_payment_currency(self) -> str:
        """If fixed payment leg, the unit of fixed payment."""
        return self.__leg_two_fixed_payment_currency

    @leg_two_fixed_payment_currency.setter
    def leg_two_fixed_payment_currency(self, value: str):
        self._property_changed('leg_two_fixed_payment_currency')
        self.__leg_two_fixed_payment_currency = value        

    @property
    def number_of_underliers(self) -> float:
        """Total number of underliers."""
        return self.__number_of_underliers

    @number_of_underliers.setter
    def number_of_underliers(self, value: float):
        self._property_changed('number_of_underliers')
        self.__number_of_underliers = value        

    @property
    def swap_type(self) -> str:
        """Swap type of position."""
        return self.__swap_type

    @swap_type.setter
    def swap_type(self, value: str):
        self._property_changed('swap_type')
        self.__swap_type = value        

    @property
    def forecast_type(self) -> str:
        """Type of return for commodity indices. Spot for individual commodities."""
        return self.__forecast_type

    @forecast_type.setter
    def forecast_type(self, value: str):
        self._property_changed('forecast_type')
        self.__forecast_type = value        

    @property
    def sell_settle_date(self) -> datetime.date:
        """Data that the sell of securities will settle."""
        return self.__sell_settle_date

    @sell_settle_date.setter
    def sell_settle_date(self, value: datetime.date):
        self._property_changed('sell_settle_date')
        self.__sell_settle_date = value        

    @property
    def new_ideas_ytd(self) -> float:
        """Ideas received by clients Year to date."""
        return self.__new_ideas_ytd

    @new_ideas_ytd.setter
    def new_ideas_ytd(self, value: float):
        self._property_changed('new_ideas_ytd')
        self.__new_ideas_ytd = value        

    @property
    def management_fee(self) -> Union[Op, float]:
        return self.__management_fee

    @management_fee.setter
    def management_fee(self, value: Union[Op, float]):
        self._property_changed('management_fee')
        self.__management_fee = value        

    @property
    def open(self) -> float:
        """Opening level of an asset based on official exchange fixing or calculation agent
           marked level."""
        return self.__open

    @open.setter
    def open(self, value: float):
        self._property_changed('open')
        self.__open = value        

    @property
    def source_id(self) -> str:
        """Unique id of data provider."""
        return self.__source_id

    @source_id.setter
    def source_id(self, value: str):
        self._property_changed('source_id')
        self.__source_id = value        

    @property
    def cusip(self) -> str:
        """CUSIP - Committee on Uniform Securities Identification Procedures number
           (subject to licensing)."""
        return self.__cusip

    @cusip.setter
    def cusip(self, value: str):
        self._property_changed('cusip')
        self.__cusip = value        

    @property
    def idea_activity_time(self) -> datetime.datetime:
        """The time the idea activity took place. If ideaStatus is open, the time reflects
           the Idea creation time. If ideaStatus is closed, the time reflects
           the time the idea was closed."""
        return self.__idea_activity_time

    @idea_activity_time.setter
    def idea_activity_time(self, value: datetime.datetime):
        self._property_changed('idea_activity_time')
        self.__idea_activity_time = value        

    @property
    def touch_spread_score(self) -> float:
        """Z-score of the difference between highest bid and lowest offer."""
        return self.__touch_spread_score

    @touch_spread_score.setter
    def touch_spread_score(self, value: float):
        self._property_changed('touch_spread_score')
        self.__touch_spread_score = value        

    @property
    def spread_option_atm_fwd_rate(self) -> float:
        """Spread Option ATM forward rate."""
        return self.__spread_option_atm_fwd_rate

    @spread_option_atm_fwd_rate.setter
    def spread_option_atm_fwd_rate(self, value: float):
        self._property_changed('spread_option_atm_fwd_rate')
        self.__spread_option_atm_fwd_rate = value        

    @property
    def net_exposure(self) -> float:
        """The difference between long and short exposure in the portfolio. If you are $60
           short and $40 long, then the netExposure would be -$20 (-60+40)."""
        return self.__net_exposure

    @net_exposure.setter
    def net_exposure(self, value: float):
        self._property_changed('net_exposure')
        self.__net_exposure = value        

    @property
    def frequency(self) -> str:
        """Requested frequency of data delivery."""
        return self.__frequency

    @frequency.setter
    def frequency(self, value: str):
        self._property_changed('frequency')
        self.__frequency = value        

    @property
    def activity_id(self) -> str:
        """Marquee unique Activity identifier."""
        return self.__activity_id

    @activity_id.setter
    def activity_id(self, value: str):
        self._property_changed('activity_id')
        self.__activity_id = value        

    @property
    def estimated_impact(self) -> float:
        """Likely impact of a proposed trade on the price of an asset (bps). The model's
           shortfall estimates reflect how much it cost to execute similar
           trades in the past, as opposed to providing a hypothetical cost
           derived using tick data."""
        return self.__estimated_impact

    @estimated_impact.setter
    def estimated_impact(self, value: float):
        self._property_changed('estimated_impact')
        self.__estimated_impact = value        

    @property
    def loan_spread_bucket(self) -> str:
        """The difference between the investment rate on cash collateral and the rebate
           rate of a loan."""
        return self.__loan_spread_bucket

    @loan_spread_bucket.setter
    def loan_spread_bucket(self, value: str):
        self._property_changed('loan_spread_bucket')
        self.__loan_spread_bucket = value        

    @property
    def event_description(self) -> str:
        """Short description of the event, providing additional information beyond
           eventType."""
        return self.__event_description

    @event_description.setter
    def event_description(self, value: str):
        self._property_changed('event_description')
        self.__event_description = value        

    @property
    def provide_non_display_tape_a(self) -> float:
        """Goldman's rate for non-displayed liquidity providing trades on tape A."""
        return self.__provide_non_display_tape_a

    @provide_non_display_tape_a.setter
    def provide_non_display_tape_a(self, value: float):
        self._property_changed('provide_non_display_tape_a')
        self.__provide_non_display_tape_a = value        

    @property
    def strike_reference(self) -> str:
        """Reference for strike level (enum: spot, forward)."""
        return self.__strike_reference

    @strike_reference.setter
    def strike_reference(self, value: str):
        self._property_changed('strike_reference')
        self.__strike_reference = value        

    @property
    def details(self) -> str:
        """Corporate action details."""
        return self.__details

    @details.setter
    def details(self, value: str):
        self._property_changed('details')
        self.__details = value        

    @property
    def provide_non_display_tape_c(self) -> float:
        """Goldman's rate for non-displayed liquidity providing trades on tape C."""
        return self.__provide_non_display_tape_c

    @provide_non_display_tape_c.setter
    def provide_non_display_tape_c(self, value: float):
        self._property_changed('provide_non_display_tape_c')
        self.__provide_non_display_tape_c = value        

    @property
    def asset_count(self) -> float:
        """Number of assets in a portfolio or index."""
        return self.__asset_count

    @asset_count.setter
    def asset_count(self, value: float):
        self._property_changed('asset_count')
        self.__asset_count = value        

    @property
    def provide_non_display_tape_b(self) -> float:
        """Goldman's rate for non-displayed liquidity providing trades on tape B."""
        return self.__provide_non_display_tape_b

    @provide_non_display_tape_b.setter
    def provide_non_display_tape_b(self, value: float):
        self._property_changed('provide_non_display_tape_b')
        self.__provide_non_display_tape_b = value        

    @property
    def sector(self) -> str:
        """The risk model sector of the stock."""
        return self.__sector

    @sector.setter
    def sector(self, value: str):
        self._property_changed('sector')
        self.__sector = value        

    @property
    def fundamental_metric(self) -> float:
        """Fundamental metric value."""
        return self.__fundamental_metric

    @fundamental_metric.setter
    def fundamental_metric(self, value: float):
        self._property_changed('fundamental_metric')
        self.__fundamental_metric = value        

    @property
    def absolute_value(self) -> float:
        """The notional value of the asset."""
        return self.__absolute_value

    @absolute_value.setter
    def absolute_value(self, value: float):
        self._property_changed('absolute_value')
        self.__absolute_value = value        

    @property
    def closing_report(self) -> str:
        """Report that was published when the trade idea was closed."""
        return self.__closing_report

    @closing_report.setter
    def closing_report(self, value: str):
        self._property_changed('closing_report')
        self.__closing_report = value        

    @property
    def mctr(self) -> float:
        """Marginal contribution of a given asset to portfolio variance, is dependent on
           covariance matrix."""
        return self.__mctr

    @mctr.setter
    def mctr(self, value: float):
        self._property_changed('mctr')
        self.__mctr = value        

    @property
    def historical_close(self) -> float:
        """Historical Close Price."""
        return self.__historical_close

    @historical_close.setter
    def historical_close(self, value: float):
        self._property_changed('historical_close')
        self.__historical_close = value        

    @property
    def asset_count_priced(self) -> float:
        """Number of assets in a portfolio which could be priced."""
        return self.__asset_count_priced

    @asset_count_priced.setter
    def asset_count_priced(self, value: float):
        self._property_changed('asset_count_priced')
        self.__asset_count_priced = value        

    @property
    def idea_id(self) -> str:
        """Marquee unique trade idea identifier."""
        return self.__idea_id

    @idea_id.setter
    def idea_id(self, value: str):
        self._property_changed('idea_id')
        self.__idea_id = value        

    @property
    def comment_status(self) -> str:
        """Corporate action comment status."""
        return self.__comment_status

    @comment_status.setter
    def comment_status(self, value: str):
        self._property_changed('comment_status')
        self.__comment_status = value        

    @property
    def marginal_cost(self) -> float:
        """Marginal cost."""
        return self.__marginal_cost

    @marginal_cost.setter
    def marginal_cost(self, value: float):
        self._property_changed('marginal_cost')
        self.__marginal_cost = value        

    @property
    def settlement_currency(self) -> str:
        """The settlement currency type for SB swap transactions in the FX asset class."""
        return self.__settlement_currency

    @settlement_currency.setter
    def settlement_currency(self, value: str):
        self._property_changed('settlement_currency')
        self.__settlement_currency = value        

    @property
    def indication_of_collateralization(self) -> str:
        """If an SB swap is not cleared, an indication of whether a swap is
           Uncollateralized (UC), Partially Collateralized (PC), One-Way
           Collateralized (OC), or Fully Collateralized (FC)."""
        return self.__indication_of_collateralization

    @indication_of_collateralization.setter
    def indication_of_collateralization(self, value: str):
        self._property_changed('indication_of_collateralization')
        self.__indication_of_collateralization = value        

    @property
    def liq_wkly(self) -> float:
        """Percent of assets that could be quickly and easily converted into investable
           cash without loss of value within a week."""
        return self.__liq_wkly

    @liq_wkly.setter
    def liq_wkly(self, value: float):
        self._property_changed('liq_wkly')
        self.__liq_wkly = value        

    @property
    def lending_partner_fee(self) -> float:
        """Fee earned by the Lending Partner in a securities lending agreement."""
        return self.__lending_partner_fee

    @lending_partner_fee.setter
    def lending_partner_fee(self, value: float):
        self._property_changed('lending_partner_fee')
        self.__lending_partner_fee = value        

    @property
    def region(self) -> str:
        """Regional classification for the asset"""
        return self.__region

    @region.setter
    def region(self, value: str):
        self._property_changed('region')
        self.__region = value        

    @property
    def option_premium(self) -> float:
        """An indication of the market value of the option at the time of execution."""
        return self.__option_premium

    @option_premium.setter
    def option_premium(self, value: float):
        self._property_changed('option_premium')
        self.__option_premium = value        

    @property
    def owner_name(self) -> str:
        """Name of person submitting request."""
        return self.__owner_name

    @owner_name.setter
    def owner_name(self, value: str):
        self._property_changed('owner_name')
        self.__owner_name = value        

    @property
    def last_updated_by_id(self) -> str:
        """Unique identifier of user who last updated the object"""
        return self.__last_updated_by_id

    @last_updated_by_id.setter
    def last_updated_by_id(self, value: str):
        self._property_changed('last_updated_by_id')
        self.__last_updated_by_id = value        

    @property
    def z_score(self) -> float:
        """Z Score."""
        return self.__z_score

    @z_score.setter
    def z_score(self, value: float):
        self._property_changed('z_score')
        self.__z_score = value        

    @property
    def legal_entity_acct(self) -> str:
        """Account assoicated with the entity that has legal rights to the fund."""
        return self.__legal_entity_acct

    @legal_entity_acct.setter
    def legal_entity_acct(self, value: str):
        self._property_changed('legal_entity_acct')
        self.__legal_entity_acct = value        

    @property
    def target_shareholder_meeting_date(self) -> str:
        """Target acquisition entity shareholder meeting date."""
        return self.__target_shareholder_meeting_date

    @target_shareholder_meeting_date.setter
    def target_shareholder_meeting_date(self, value: str):
        self._property_changed('target_shareholder_meeting_date')
        self.__target_shareholder_meeting_date = value        

    @property
    def event_start_time(self) -> str:
        """The start time of the event if the event occurs during a time window and the
           event has a specific start time. It is represented in HH:MM 24 hour
           format in the time zone of the exchange where the company is listed."""
        return self.__event_start_time

    @event_start_time.setter
    def event_start_time(self, value: str):
        self._property_changed('event_start_time')
        self.__event_start_time = value        

    @property
    def turnover(self) -> float:
        """Turnover."""
        return self.__turnover

    @turnover.setter
    def turnover(self, value: float):
        self._property_changed('turnover')
        self.__turnover = value        

    @property
    def price_spot_target_unit(self) -> str:
        """Unit in which the target price is reported."""
        return self.__price_spot_target_unit

    @price_spot_target_unit.setter
    def price_spot_target_unit(self, value: str):
        self._property_changed('price_spot_target_unit')
        self.__price_spot_target_unit = value        

    @property
    def compliance_effective_time(self) -> datetime.datetime:
        """Time that the compliance status became effective."""
        return self.__compliance_effective_time

    @compliance_effective_time.setter
    def compliance_effective_time(self, value: datetime.datetime):
        self._property_changed('compliance_effective_time')
        self.__compliance_effective_time = value        

    @property
    def expiration_date(self) -> datetime.date:
        """The expiration date of the associated contract and the last date it trades."""
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value: datetime.date):
        self._property_changed('expiration_date')
        self.__expiration_date = value        

    @property
    def leg_one_type(self) -> str:
        """Indication if leg 1 is fixed or floating or Physical."""
        return self.__leg_one_type

    @leg_one_type.setter
    def leg_one_type(self, value: str):
        self._property_changed('leg_one_type')
        self.__leg_one_type = value        

    @property
    def leg_two_spread(self) -> float:
        """Spread of leg."""
        return self.__leg_two_spread

    @leg_two_spread.setter
    def leg_two_spread(self, value: float):
        self._property_changed('leg_two_spread')
        self.__leg_two_spread = value        

    @property
    def coverage(self) -> str:
        """Coverage of dataset."""
        return self.__coverage

    @coverage.setter
    def coverage(self, value: str):
        self._property_changed('coverage')
        self.__coverage = value        

    @property
    def g_percentile(self) -> float:
        """Percentile based on G score."""
        return self.__g_percentile

    @g_percentile.setter
    def g_percentile(self, value: float):
        self._property_changed('g_percentile')
        self.__g_percentile = value        

    @property
    def lending_fund_nav(self) -> float:
        """Net Asset Value of a securities lending fund."""
        return self.__lending_fund_nav

    @lending_fund_nav.setter
    def lending_fund_nav(self, value: float):
        self._property_changed('lending_fund_nav')
        self.__lending_fund_nav = value        

    @property
    def source_original_category(self) -> str:
        """Source category's original name."""
        return self.__source_original_category

    @source_original_category.setter
    def source_original_category(self, value: str):
        self._property_changed('source_original_category')
        self.__source_original_category = value        

    @property
    def composite5_day_adv(self) -> float:
        """Composite 5 day ADV."""
        return self.__composite5_day_adv

    @composite5_day_adv.setter
    def composite5_day_adv(self, value: float):
        self._property_changed('composite5_day_adv')
        self.__composite5_day_adv = value        

    @property
    def marginal_contribution_to_risk(self) -> float:
        """Marginal contribution of a given asset to portfolio variance, is dependent on
           covariance matrix."""
        return self.__marginal_contribution_to_risk

    @marginal_contribution_to_risk.setter
    def marginal_contribution_to_risk(self, value: float):
        self._property_changed('marginal_contribution_to_risk')
        self.__marginal_contribution_to_risk = value        

    @property
    def latest_execution_time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__latest_execution_time

    @latest_execution_time.setter
    def latest_execution_time(self, value: datetime.datetime):
        self._property_changed('latest_execution_time')
        self.__latest_execution_time = value        

    @property
    def close_date(self) -> datetime.date:
        """Date the trade idea was closed."""
        return self.__close_date

    @close_date.setter
    def close_date(self, value: datetime.date):
        self._property_changed('close_date')
        self.__close_date = value        

    @property
    def new_ideas_wtd(self) -> float:
        """Ideas received by clients Week to date."""
        return self.__new_ideas_wtd

    @new_ideas_wtd.setter
    def new_ideas_wtd(self, value: float):
        self._property_changed('new_ideas_wtd')
        self.__new_ideas_wtd = value        

    @property
    def asset_class_sdr(self) -> str:
        """An indication of one of the broad categories. For our use case will typically be
           CO."""
        return self.__asset_class_sdr

    @asset_class_sdr.setter
    def asset_class_sdr(self, value: str):
        self._property_changed('asset_class_sdr')
        self.__asset_class_sdr = value        

    @property
    def comment(self) -> str:
        """The comment associated with the trade idea in URL encoded format."""
        return self.__comment

    @comment.setter
    def comment(self, value: str):
        self._property_changed('comment')
        self.__comment = value        

    @property
    def source_symbol(self) -> str:
        """Source symbol."""
        return self.__source_symbol

    @source_symbol.setter
    def source_symbol(self, value: str):
        self._property_changed('source_symbol')
        self.__source_symbol = value        

    @property
    def scenario_id(self) -> str:
        """Marquee unique scenario identifier"""
        return self.__scenario_id

    @scenario_id.setter
    def scenario_id(self, value: str):
        self._property_changed('scenario_id')
        self.__scenario_id = value        

    @property
    def ask_unadjusted(self) -> float:
        """Unadjusted ask level of an asset based on official exchange fixing or
           calculation agent marked level."""
        return self.__ask_unadjusted

    @ask_unadjusted.setter
    def ask_unadjusted(self, value: float):
        self._property_changed('ask_unadjusted')
        self.__ask_unadjusted = value        

    @property
    def termination_tenor(self) -> str:
        """Tenor"""
        return self.__termination_tenor

    @termination_tenor.setter
    def termination_tenor(self, value: str):
        self._property_changed('termination_tenor')
        self.__termination_tenor = value        

    @property
    def queue_clock_time(self) -> float:
        """The Queue Clock Time of the stock  on the particular date."""
        return self.__queue_clock_time

    @queue_clock_time.setter
    def queue_clock_time(self, value: float):
        self._property_changed('queue_clock_time')
        self.__queue_clock_time = value        

    @property
    def restrict_external_derived_data(self) -> bool:
        """Restricts Ability to Use Externally as Part of Derived Data."""
        return self.__restrict_external_derived_data

    @restrict_external_derived_data.setter
    def restrict_external_derived_data(self, value: bool):
        self._property_changed('restrict_external_derived_data')
        self.__restrict_external_derived_data = value        

    @property
    def ask_change(self) -> float:
        """Change in the ask price."""
        return self.__ask_change

    @ask_change.setter
    def ask_change(self, value: float):
        self._property_changed('ask_change')
        self.__ask_change = value        

    @property
    def tcm_cost_participation_rate50_pct(self) -> float:
        """TCM cost with a 50 percent participation rate."""
        return self.__tcm_cost_participation_rate50_pct

    @tcm_cost_participation_rate50_pct.setter
    def tcm_cost_participation_rate50_pct(self, value: float):
        self._property_changed('tcm_cost_participation_rate50_pct')
        self.__tcm_cost_participation_rate50_pct = value        

    @property
    def end_date(self) -> datetime.date:
        """The maturity, termination, or end date of the reportable SB swap transaction."""
        return self.__end_date

    @end_date.setter
    def end_date(self, value: datetime.date):
        self._property_changed('end_date')
        self.__end_date = value        

    @property
    def contract_type(self) -> str:
        """Contract type."""
        return self.__contract_type

    @contract_type.setter
    def contract_type(self, value: str):
        self._property_changed('contract_type')
        self.__contract_type = value        

    @property
    def type(self) -> str:
        """Asset type differentiates the product categorization or contract type"""
        return self.__type

    @type.setter
    def type(self, value: str):
        self._property_changed('type')
        self.__type = value        

    @property
    def strike_ref(self) -> str:
        """Reference for strike level (enum: spot, forward,delta_call, delta_put,
           delta_neutral)."""
        return self.__strike_ref

    @strike_ref.setter
    def strike_ref(self, value: str):
        self._property_changed('strike_ref')
        self.__strike_ref = value        

    @property
    def cumulative_pnl(self) -> float:
        """Cumulative PnL from the start date to the current date."""
        return self.__cumulative_pnl

    @cumulative_pnl.setter
    def cumulative_pnl(self, value: float):
        self._property_changed('cumulative_pnl')
        self.__cumulative_pnl = value        

    @property
    def loss(self) -> float:
        """Loss price component."""
        return self.__loss

    @loss.setter
    def loss(self, value: float):
        self._property_changed('loss')
        self.__loss = value        

    @property
    def unadjusted_volume(self) -> float:
        """Unadjusted volume traded."""
        return self.__unadjusted_volume

    @unadjusted_volume.setter
    def unadjusted_volume(self, value: float):
        self._property_changed('unadjusted_volume')
        self.__unadjusted_volume = value        

    @property
    def midcurve_vol(self) -> float:
        """Historical implied normal volatility for a liquid point on midcurve vol surface."""
        return self.__midcurve_vol

    @midcurve_vol.setter
    def midcurve_vol(self, value: float):
        self._property_changed('midcurve_vol')
        self.__midcurve_vol = value        

    @property
    def trading_cost_pnl(self) -> float:
        """Trading cost profit and loss (PNL)."""
        return self.__trading_cost_pnl

    @trading_cost_pnl.setter
    def trading_cost_pnl(self, value: float):
        self._property_changed('trading_cost_pnl')
        self.__trading_cost_pnl = value        

    @property
    def price_notation_type(self) -> str:
        """Basis points, Price, Yield, Spread, Coupon, etc., depending on the type of SB
           swap, which is calculated at affirmation."""
        return self.__price_notation_type

    @price_notation_type.setter
    def price_notation_type(self, value: str):
        self._property_changed('price_notation_type')
        self.__price_notation_type = value        

    @property
    def payment_quantity(self) -> float:
        """Quantity in the payment currency."""
        return self.__payment_quantity

    @payment_quantity.setter
    def payment_quantity(self, value: float):
        self._property_changed('payment_quantity')
        self.__payment_quantity = value        

    @property
    def position_idx(self) -> int:
        """The index of the corresponding position in the risk request."""
        return self.__position_idx

    @position_idx.setter
    def position_idx(self, value: int):
        self._property_changed('position_idx')
        self.__position_idx = value        

    @property
    def implied_volatility_by_relative_strike(self) -> float:
        """Volatility of an asset implied by observations of market prices."""
        return self.__implied_volatility_by_relative_strike

    @implied_volatility_by_relative_strike.setter
    def implied_volatility_by_relative_strike(self, value: float):
        self._property_changed('implied_volatility_by_relative_strike')
        self.__implied_volatility_by_relative_strike = value        

    @property
    def percent_adv(self) -> float:
        """Size of trade as percentage of average daily volume (e.g. .05, 1, 2, ..., 20)."""
        return self.__percent_adv

    @percent_adv.setter
    def percent_adv(self, value: float):
        self._property_changed('percent_adv')
        self.__percent_adv = value        

    @property
    def sub_region(self) -> str:
        """Filter by any identifier of an asset like ticker, bloomberg id etc."""
        return self.__sub_region

    @sub_region.setter
    def sub_region(self, value: str):
        self._property_changed('sub_region')
        self.__sub_region = value        

    @property
    def contract(self) -> str:
        """Contract month code and year (e.g. F18)."""
        return self.__contract

    @contract.setter
    def contract(self, value: str):
        self._property_changed('contract')
        self.__contract = value        

    @property
    def payment_frequency1(self) -> str:
        """An integer multiplier of a time period describing how often the parties to the
           SB swap transaction exchange payments associated with each party???s
           obligation. Such payment frequency may be described as one letter
           preceded by an integer."""
        return self.__payment_frequency1

    @payment_frequency1.setter
    def payment_frequency1(self, value: str):
        self._property_changed('payment_frequency1')
        self.__payment_frequency1 = value        

    @property
    def payment_frequency2(self) -> str:
        """Same as Payment Frequency 1."""
        return self.__payment_frequency2

    @payment_frequency2.setter
    def payment_frequency2(self, value: str):
        self._property_changed('payment_frequency2')
        self.__payment_frequency2 = value        

    @property
    def bespoke(self) -> str:
        """Indication if the trade is bespoke."""
        return self.__bespoke

    @bespoke.setter
    def bespoke(self, value: str):
        self._property_changed('bespoke')
        self.__bespoke = value        

    @property
    def repo_tenor(self) -> str:
        """Maturity of repurchase agreement."""
        return self.__repo_tenor

    @repo_tenor.setter
    def repo_tenor(self, value: str):
        self._property_changed('repo_tenor')
        self.__repo_tenor = value        

    @property
    def quality_stars(self) -> float:
        """Confidence in the BPE."""
        return self.__quality_stars

    @quality_stars.setter
    def quality_stars(self, value: float):
        self._property_changed('quality_stars')
        self.__quality_stars = value        

    @property
    def source_ticker(self) -> str:
        """Source ticker."""
        return self.__source_ticker

    @source_ticker.setter
    def source_ticker(self, value: str):
        self._property_changed('source_ticker')
        self.__source_ticker = value        

    @property
    def lending_fund(self) -> str:
        """Name of the lending fund on a securities lending agreement."""
        return self.__lending_fund

    @lending_fund.setter
    def lending_fund(self, value: str):
        self._property_changed('lending_fund')
        self.__lending_fund = value        

    @property
    def tcm_cost_participation_rate15_pct(self) -> float:
        """TCM cost with a 15 percent participation rate."""
        return self.__tcm_cost_participation_rate15_pct

    @tcm_cost_participation_rate15_pct.setter
    def tcm_cost_participation_rate15_pct(self, value: float):
        self._property_changed('tcm_cost_participation_rate15_pct')
        self.__tcm_cost_participation_rate15_pct = value        

    @property
    def sensitivity(self) -> float:
        """Sensitivity."""
        return self.__sensitivity

    @sensitivity.setter
    def sensitivity(self, value: float):
        self._property_changed('sensitivity')
        self.__sensitivity = value        

    @property
    def fiscal_year(self) -> str:
        """The Calendar Year."""
        return self.__fiscal_year

    @fiscal_year.setter
    def fiscal_year(self, value: str):
        self._property_changed('fiscal_year')
        self.__fiscal_year = value        

    @property
    def recall_date(self) -> datetime.date:
        """The date at which the securities on loan were recalled."""
        return self.__recall_date

    @recall_date.setter
    def recall_date(self, value: datetime.date):
        self._property_changed('recall_date')
        self.__recall_date = value        

    @property
    def internal(self) -> bool:
        """Whether request came from internal or external."""
        return self.__internal

    @internal.setter
    def internal(self, value: bool):
        self._property_changed('internal')
        self.__internal = value        

    @property
    def adjusted_bid_price(self) -> float:
        """Latest Bid Price (price willing to buy) adjusted for corporate actions."""
        return self.__adjusted_bid_price

    @adjusted_bid_price.setter
    def adjusted_bid_price(self, value: float):
        self._property_changed('adjusted_bid_price')
        self.__adjusted_bid_price = value        

    @property
    def var_swap(self) -> float:
        """Strike such that the price of an uncapped variance swap on the underlying index
           is zero at inception."""
        return self.__var_swap

    @var_swap.setter
    def var_swap(self, value: float):
        self._property_changed('var_swap')
        self.__var_swap = value        

    @property
    def fixed_payment_leg2(self) -> float:
        """If fixed payment leg, the fixed payment amount, which is price*number of
           contracts bought*contract unit."""
        return self.__fixed_payment_leg2

    @fixed_payment_leg2.setter
    def fixed_payment_leg2(self, value: float):
        self._property_changed('fixed_payment_leg2')
        self.__fixed_payment_leg2 = value        

    @property
    def fixed_payment_leg1(self) -> float:
        """If fixed payment leg, the fixed payment amount, which is price*number of
           contracts bought*contract unit."""
        return self.__fixed_payment_leg1

    @fixed_payment_leg1.setter
    def fixed_payment_leg1(self, value: float):
        self._property_changed('fixed_payment_leg1')
        self.__fixed_payment_leg1 = value        

    @property
    def low_unadjusted(self) -> float:
        """Unadjusted low level of an asset based on official exchange fixing or
           calculation agent marked level."""
        return self.__low_unadjusted

    @low_unadjusted.setter
    def low_unadjusted(self, value: float):
        self._property_changed('low_unadjusted')
        self.__low_unadjusted = value        

    @property
    def original_dissemination_id(self) -> str:
        """On cancellations and corrections, this ID will hold the Dissemination ID of the
           originally published real-time message."""
        return self.__original_dissemination_id

    @original_dissemination_id.setter
    def original_dissemination_id(self, value: str):
        self._property_changed('original_dissemination_id')
        self.__original_dissemination_id = value        

    @property
    def macs_secondary_asset_class(self) -> str:
        """Indicates the secondary asset class the multi asset class swap falls under."""
        return self.__macs_secondary_asset_class

    @macs_secondary_asset_class.setter
    def macs_secondary_asset_class(self, value: str):
        self._property_changed('macs_secondary_asset_class')
        self.__macs_secondary_asset_class = value        

    @property
    def leg_two_averaging_method(self) -> str:
        """Averaging method of leg."""
        return self.__leg_two_averaging_method

    @leg_two_averaging_method.setter
    def leg_two_averaging_method(self, value: str):
        self._property_changed('leg_two_averaging_method')
        self.__leg_two_averaging_method = value        

    @property
    def sectors_raw(self) -> Tuple[str, ...]:
        """Sector classifications of an asset."""
        return self.__sectors_raw

    @sectors_raw.setter
    def sectors_raw(self, value: Tuple[str, ...]):
        self._property_changed('sectors_raw')
        self.__sectors_raw = value        

    @property
    def shareclass_price(self) -> float:
        """Price of the shareclass on a certain day."""
        return self.__shareclass_price

    @shareclass_price.setter
    def shareclass_price(self, value: float):
        self._property_changed('shareclass_price')
        self.__shareclass_price = value        

    @property
    def integrated_score(self) -> float:
        """Average of the Growth, Financial Returns and (1-Multiple) percentile (a higher
           score means more attractive)."""
        return self.__integrated_score

    @integrated_score.setter
    def integrated_score(self, value: float):
        self._property_changed('integrated_score')
        self.__integrated_score = value        

    @property
    def trade_size(self) -> float:
        """Size of trade ($mm)."""
        return self.__trade_size

    @trade_size.setter
    def trade_size(self, value: float):
        self._property_changed('trade_size')
        self.__trade_size = value        

    @property
    def price_spot_entry_value(self) -> float:
        """Opening price value of the trade idea."""
        return self.__price_spot_entry_value

    @price_spot_entry_value.setter
    def price_spot_entry_value(self, value: float):
        self._property_changed('price_spot_entry_value')
        self.__price_spot_entry_value = value        

    @property
    def symbol_dimensions(self) -> Tuple[str, ...]:
        """Set of fields that determine database table name."""
        return self.__symbol_dimensions

    @symbol_dimensions.setter
    def symbol_dimensions(self, value: Tuple[str, ...]):
        self._property_changed('symbol_dimensions')
        self.__symbol_dimensions = value        

    @property
    def index_location_leg1(self) -> str:
        """Location of leg."""
        return self.__index_location_leg1

    @index_location_leg1.setter
    def index_location_leg1(self, value: str):
        self._property_changed('index_location_leg1')
        self.__index_location_leg1 = value        

    @property
    def index_location_leg2(self) -> str:
        """Location of leg."""
        return self.__index_location_leg2

    @index_location_leg2.setter
    def index_location_leg2(self, value: str):
        self._property_changed('index_location_leg2')
        self.__index_location_leg2 = value        

    @property
    def option_type_sdr(self) -> str:
        """An indication of the type of the option."""
        return self.__option_type_sdr

    @option_type_sdr.setter
    def option_type_sdr(self, value: str):
        self._property_changed('option_type_sdr')
        self.__option_type_sdr = value        

    @property
    def scenario_group_id(self) -> str:
        """Marquee unique scenario group identifier"""
        return self.__scenario_group_id

    @scenario_group_id.setter
    def scenario_group_id(self, value: str):
        self._property_changed('scenario_group_id')
        self.__scenario_group_id = value        

    @property
    def avg_yield7_day(self) -> float:
        """Only used for GS Money Market funds, assumes sum of the past 7 days, divided by
           7, and expressed as a percent."""
        return self.__avg_yield7_day

    @avg_yield7_day.setter
    def avg_yield7_day(self, value: float):
        self._property_changed('avg_yield7_day')
        self.__avg_yield7_day = value        

    @property
    def average_implied_variance(self) -> float:
        """Average variance of an asset implied by observations of market prices."""
        return self.__average_implied_variance

    @average_implied_variance.setter
    def average_implied_variance(self, value: float):
        self._property_changed('average_implied_variance')
        self.__average_implied_variance = value        

    @property
    def averaging_method_leg2(self) -> str:
        """Averaging method of leg."""
        return self.__averaging_method_leg2

    @averaging_method_leg2.setter
    def averaging_method_leg2(self, value: str):
        self._property_changed('averaging_method_leg2')
        self.__averaging_method_leg2 = value        

    @property
    def avg_trade_rate_description(self) -> str:
        """Description of the Stock's Average Trading Rate on the particular date."""
        return self.__avg_trade_rate_description

    @avg_trade_rate_description.setter
    def avg_trade_rate_description(self, value: str):
        self._property_changed('avg_trade_rate_description')
        self.__avg_trade_rate_description = value        

    @property
    def averaging_method_leg1(self) -> str:
        """Averaging method of leg."""
        return self.__averaging_method_leg1

    @averaging_method_leg1.setter
    def averaging_method_leg1(self, value: str):
        self._property_changed('averaging_method_leg1')
        self.__averaging_method_leg1 = value        

    @property
    def fraction(self) -> float:
        """Fraction."""
        return self.__fraction

    @fraction.setter
    def fraction(self, value: float):
        self._property_changed('fraction')
        self.__fraction = value        

    @property
    def asset_count_short(self) -> float:
        """Number of assets in a portfolio with short exposure."""
        return self.__asset_count_short

    @asset_count_short.setter
    def asset_count_short(self, value: float):
        self._property_changed('asset_count_short')
        self.__asset_count_short = value        

    @property
    def collateral_percentage_required(self) -> float:
        """Collateral percentage requied to cover the given position."""
        return self.__collateral_percentage_required

    @collateral_percentage_required.setter
    def collateral_percentage_required(self, value: float):
        self._property_changed('collateral_percentage_required')
        self.__collateral_percentage_required = value        

    @property
    def opening_auction(self) -> float:
        """Goldman's rate for trades on the opening auction."""
        return self.__opening_auction

    @opening_auction.setter
    def opening_auction(self, value: float):
        self._property_changed('opening_auction')
        self.__opening_auction = value        

    @property
    def date(self) -> datetime.date:
        """ISO 8601 formatted date."""
        return self.__date

    @date.setter
    def date(self, value: datetime.date):
        self._property_changed('date')
        self.__date = value        

    @property
    def total_std_return_since_inception(self) -> float:
        """Average annual total returns as of most recent calendar quarter-end."""
        return self.__total_std_return_since_inception

    @total_std_return_since_inception.setter
    def total_std_return_since_inception(self, value: float):
        self._property_changed('total_std_return_since_inception')
        self.__total_std_return_since_inception = value        

    @property
    def high_unadjusted(self) -> float:
        """Unadjusted high level of an asset based on official exchange fixing or
           calculation agent marked level."""
        return self.__high_unadjusted

    @high_unadjusted.setter
    def high_unadjusted(self, value: float):
        self._property_changed('high_unadjusted')
        self.__high_unadjusted = value        

    @property
    def source_category(self) -> str:
        """Source category of event."""
        return self.__source_category

    @source_category.setter
    def source_category(self, value: str):
        self._property_changed('source_category')
        self.__source_category = value        

    @property
    def tv_product_mnemonic(self) -> str:
        """Unique by Trade Vault Product based on Product Taxonomy."""
        return self.__tv_product_mnemonic

    @tv_product_mnemonic.setter
    def tv_product_mnemonic(self, value: str):
        self._property_changed('tv_product_mnemonic')
        self.__tv_product_mnemonic = value        

    @property
    def volume_unadjusted(self) -> float:
        """Unadjusted volume traded."""
        return self.__volume_unadjusted

    @volume_unadjusted.setter
    def volume_unadjusted(self, value: float):
        self._property_changed('volume_unadjusted')
        self.__volume_unadjusted = value        

    @property
    def price_to_earnings(self) -> float:
        """Price to earnings."""
        return self.__price_to_earnings

    @price_to_earnings.setter
    def price_to_earnings(self, value: float):
        self._property_changed('price_to_earnings')
        self.__price_to_earnings = value        

    @property
    def avg_trade_rate_label(self):
        return self.__avg_trade_rate_label

    @avg_trade_rate_label.setter
    def avg_trade_rate_label(self, value):
        self._property_changed('avg_trade_rate_label')
        self.__avg_trade_rate_label = value        

    @property
    def ann_yield3_month(self) -> float:
        """Calculates the total return for 3 months, representing past performance."""
        return self.__ann_yield3_month

    @ann_yield3_month.setter
    def ann_yield3_month(self, value: float):
        self._property_changed('ann_yield3_month')
        self.__ann_yield3_month = value        

    @property
    def net_flow_std(self) -> float:
        """Net flow for the asset in standard deviations."""
        return self.__net_flow_std

    @net_flow_std.setter
    def net_flow_std(self, value: float):
        self._property_changed('net_flow_std')
        self.__net_flow_std = value        

    @property
    def ask_size(self) -> float:
        """The number of shares, lots, or contracts willing to sell at the Ask price."""
        return self.__ask_size

    @ask_size.setter
    def ask_size(self, value: float):
        self._property_changed('ask_size')
        self.__ask_size = value        

    @property
    def std30_days_unsubsidized_yield(self) -> float:
        """Average annual total returns as of most recent calendar quarter-end."""
        return self.__std30_days_unsubsidized_yield

    @std30_days_unsubsidized_yield.setter
    def std30_days_unsubsidized_yield(self, value: float):
        self._property_changed('std30_days_unsubsidized_yield')
        self.__std30_days_unsubsidized_yield = value        

    @property
    def resource(self) -> str:
        """The event resource. For example: Asset"""
        return self.__resource

    @resource.setter
    def resource(self, value: str):
        self._property_changed('resource')
        self.__resource = value        

    @property
    def dissemination_time(self) -> datetime.datetime:
        """Time of dissemination."""
        return self.__dissemination_time

    @dissemination_time.setter
    def dissemination_time(self, value: datetime.datetime):
        self._property_changed('dissemination_time')
        self.__dissemination_time = value        

    @property
    def price_to_cash(self) -> float:
        """Price to cash."""
        return self.__price_to_cash

    @price_to_cash.setter
    def price_to_cash(self, value: float):
        self._property_changed('price_to_cash')
        self.__price_to_cash = value        

    @property
    def average_realized_volatility(self) -> float:
        """Average volatility of an asset realized by observations of market prices."""
        return self.__average_realized_volatility

    @average_realized_volatility.setter
    def average_realized_volatility(self, value: float):
        self._property_changed('average_realized_volatility')
        self.__average_realized_volatility = value        

    @property
    def nav_spread(self) -> float:
        """Net asset value spread. Quoted (running) spread (mid) of the underlying basket
           of single name CDS. (Theoretical Index value). In basis points."""
        return self.__nav_spread

    @nav_spread.setter
    def nav_spread(self, value: float):
        self._property_changed('nav_spread')
        self.__nav_spread = value        

    @property
    def bid_price(self) -> float:
        """Latest Bid Price (price willing to buy)."""
        return self.__bid_price

    @bid_price.setter
    def bid_price(self, value: float):
        self._property_changed('bid_price')
        self.__bid_price = value        

    @property
    def dollar_total_return(self) -> float:
        """The dollar total return of an instrument."""
        return self.__dollar_total_return

    @dollar_total_return.setter
    def dollar_total_return(self, value: float):
        self._property_changed('dollar_total_return')
        self.__dollar_total_return = value        

    @property
    def block_unit(self) -> str:
        """Unit of measure used for Block trades."""
        return self.__block_unit

    @block_unit.setter
    def block_unit(self, value: str):
        self._property_changed('block_unit')
        self.__block_unit = value        

    @property
    def es_numeric_percentile(self) -> float:
        """Sector relative percentile based on E&S numeric score."""
        return self.__es_numeric_percentile

    @es_numeric_percentile.setter
    def es_numeric_percentile(self, value: float):
        self._property_changed('es_numeric_percentile')
        self.__es_numeric_percentile = value        

    @property
    def repurchase_rate(self) -> float:
        """Repurchase Rate."""
        return self.__repurchase_rate

    @repurchase_rate.setter
    def repurchase_rate(self, value: float):
        self._property_changed('repurchase_rate')
        self.__repurchase_rate = value        

    @property
    def csa_terms(self) -> str:
        """CSA terms."""
        return self.__csa_terms

    @csa_terms.setter
    def csa_terms(self, value: str):
        self._property_changed('csa_terms')
        self.__csa_terms = value        

    @property
    def daily_net_shareholder_flows(self) -> float:
        """Cash dividends paid daily."""
        return self.__daily_net_shareholder_flows

    @daily_net_shareholder_flows.setter
    def daily_net_shareholder_flows(self, value: float):
        self._property_changed('daily_net_shareholder_flows')
        self.__daily_net_shareholder_flows = value        

    @property
    def ask_gspread(self) -> float:
        """Ask G spread."""
        return self.__ask_gspread

    @ask_gspread.setter
    def ask_gspread(self, value: float):
        self._property_changed('ask_gspread')
        self.__ask_gspread = value        

    @property
    def cal_spread_mis_pricing(self) -> float:
        """Futures implied funding rate relative to interest rate benchmark (usually Libor-
           based). Represents dividend-adjusted rate at which investor is
           borrowing (lending) when long (short) future."""
        return self.__cal_spread_mis_pricing

    @cal_spread_mis_pricing.setter
    def cal_spread_mis_pricing(self, value: float):
        self._property_changed('cal_spread_mis_pricing')
        self.__cal_spread_mis_pricing = value        

    @property
    def leg_two_type(self) -> str:
        """Indication if leg 2 is fixed or floating or Physical."""
        return self.__leg_two_type

    @leg_two_type.setter
    def leg_two_type(self, value: str):
        self._property_changed('leg_two_type')
        self.__leg_two_type = value        

    @property
    def rate366(self) -> float:
        """Rate with interest calculated according to the number of days in a leap year,
           366."""
        return self.__rate366

    @rate366.setter
    def rate366(self, value: float):
        self._property_changed('rate366')
        self.__rate366 = value        

    @property
    def rate365(self) -> float:
        """Rate with interest calculated according to a normal number of days in the total
           year, 365."""
        return self.__rate365

    @rate365.setter
    def rate365(self, value: float):
        self._property_changed('rate365')
        self.__rate365 = value        

    @property
    def rate360(self) -> float:
        """Rate with interest calculated according to the discount method, using the number
           of days used by banks, 360."""
        return self.__rate360

    @rate360.setter
    def rate360(self, value: float):
        self._property_changed('rate360')
        self.__rate360 = value        

    @property
    def delivery_point_leg1(self) -> str:
        """Delivery point of leg."""
        return self.__delivery_point_leg1

    @delivery_point_leg1.setter
    def delivery_point_leg1(self, value: str):
        self._property_changed('delivery_point_leg1')
        self.__delivery_point_leg1 = value        

    @property
    def opening_report(self) -> str:
        """Report that was published when the trade idea was opened."""
        return self.__opening_report

    @opening_report.setter
    def opening_report(self, value: str):
        self._property_changed('opening_report')
        self.__opening_report = value        

    @property
    def value(self) -> float:
        """The given value."""
        return self.__value

    @value.setter
    def value(self, value: float):
        self._property_changed('value')
        self.__value = value        

    @property
    def leg_one_index_location(self) -> str:
        """Location of leg."""
        return self.__leg_one_index_location

    @leg_one_index_location.setter
    def leg_one_index_location(self, value: str):
        self._property_changed('leg_one_index_location')
        self.__leg_one_index_location = value        

    @property
    def product_type(self) -> str:
        """Basket Product Type."""
        return self.__product_type

    @product_type.setter
    def product_type(self, value: str):
        self._property_changed('product_type')
        self.__product_type = value        

    @property
    def quantity(self) -> float:
        """Number of units of a given asset held within a portfolio."""
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float):
        self._property_changed('quantity')
        self.__quantity = value        

    @property
    def report_id(self) -> str:
        """Report Identifier."""
        return self.__report_id

    @report_id.setter
    def report_id(self, value: str):
        self._property_changed('report_id')
        self.__report_id = value        

    @property
    def macs_primary_asset_class(self) -> str:
        """Indicates the primary asset class the multi asset class swap falls under."""
        return self.__macs_primary_asset_class

    @macs_primary_asset_class.setter
    def macs_primary_asset_class(self, value: str):
        self._property_changed('macs_primary_asset_class')
        self.__macs_primary_asset_class = value        

    @property
    def midcurve_atm_fwd_rate(self) -> float:
        """Midcurve ATM forward rate."""
        return self.__midcurve_atm_fwd_rate

    @midcurve_atm_fwd_rate.setter
    def midcurve_atm_fwd_rate(self, value: float):
        self._property_changed('midcurve_atm_fwd_rate')
        self.__midcurve_atm_fwd_rate = value        

    @property
    def trader(self) -> str:
        """Trader name."""
        return self.__trader

    @trader.setter
    def trader(self, value: str):
        self._property_changed('trader')
        self.__trader = value        

    @property
    def equity_risk_premium_index(self) -> float:
        """Equity risk premium index: difference between cost of equity and 10y treasury
           yield."""
        return self.__equity_risk_premium_index

    @equity_risk_premium_index.setter
    def equity_risk_premium_index(self, value: float):
        self._property_changed('equity_risk_premium_index')
        self.__equity_risk_premium_index = value        

    @property
    def clearing_house(self) -> str:
        """Swap Clearing House"""
        return self.__clearing_house

    @clearing_house.setter
    def clearing_house(self, value: str):
        self._property_changed('clearing_house')
        self.__clearing_house = value        

    @property
    def valuation_date(self) -> str:
        """Specific to rates, the date a valuation is recorded."""
        return self.__valuation_date

    @valuation_date.setter
    def valuation_date(self, value: str):
        self._property_changed('valuation_date')
        self.__valuation_date = value        

    @property
    def restrict_gs_federation(self) -> bool:
        """Restricts GS Federation Visibility."""
        return self.__restrict_gs_federation

    @restrict_gs_federation.setter
    def restrict_gs_federation(self, value: bool):
        self._property_changed('restrict_gs_federation')
        self.__restrict_gs_federation = value        

    @property
    def tcm_cost_horizon6_hour(self) -> float:
        """TCM cost with a 6 hour time horizon."""
        return self.__tcm_cost_horizon6_hour

    @tcm_cost_horizon6_hour.setter
    def tcm_cost_horizon6_hour(self, value: float):
        self._property_changed('tcm_cost_horizon6_hour')
        self.__tcm_cost_horizon6_hour = value        

    @property
    def liq_dly(self) -> float:
        """Percent of assets that could be quickly and easily converted into investable
           cash without loss of value within a day."""
        return self.__liq_dly

    @liq_dly.setter
    def liq_dly(self, value: float):
        self._property_changed('liq_dly')
        self.__liq_dly = value        

    @property
    def price_to_book(self) -> float:
        """Price to book."""
        return self.__price_to_book

    @price_to_book.setter
    def price_to_book(self, value: float):
        self._property_changed('price_to_book')
        self.__price_to_book = value        

    @property
    def isin(self) -> str:
        """ISIN - International securities identifier number (subect to licensing)."""
        return self.__isin

    @isin.setter
    def isin(self, value: str):
        self._property_changed('isin')
        self.__isin = value        


class MarketDataPatternAndShock(Base):
        
    """A shock to apply to market coordinate values matching the supplied pattern"""

    @camel_case_translate
    def __init__(
        self,
        pattern: MarketDataPattern,
        shock: MarketDataShock,
        name: str = None
    ):        
        super().__init__()
        self.pattern = pattern
        self.shock = shock
        self.name = name

    @property
    def pattern(self) -> MarketDataPattern:
        """A pattern used to match market coordinates"""
        return self.__pattern

    @pattern.setter
    def pattern(self, value: MarketDataPattern):
        self._property_changed('pattern')
        self.__pattern = value        

    @property
    def shock(self) -> MarketDataShock:
        """A shock to apply to market coordinate values"""
        return self.__shock

    @shock.setter
    def shock(self, value: MarketDataShock):
        self._property_changed('shock')
        self.__shock = value        


class CSLScheduleArray(Base):
        
    """An array of schedules"""

    @camel_case_translate
    def __init__(
        self,
        schedule_values: Tuple[CSLSchedule, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.schedule_values = schedule_values
        self.name = name

    @property
    def schedule_values(self) -> Tuple[CSLSchedule, ...]:
        """A schedule"""
        return self.__schedule_values

    @schedule_values.setter
    def schedule_values(self, value: Tuple[CSLSchedule, ...]):
        self._property_changed('schedule_values')
        self.__schedule_values = value        


class MarketDataShockBasedScenario(Scenario):
        
    """A scenario comprised of user-defined market data shocks"""

    @camel_case_translate
    def __init__(
        self,
        shocks: Tuple[MarketDataPatternAndShock, ...],
        name: str = None
    ):        
        super().__init__()
        self.shocks = shocks
        self.name = name

    @property
    def scenario_type(self) -> str:
        """MarketDataShockBasedScenario"""
        return 'MarketDataShockBasedScenario'        

    @property
    def shocks(self) -> Tuple[MarketDataPatternAndShock, ...]:
        """A shock to apply to market coordinate values matching the supplied pattern"""
        return self.__shocks

    @shocks.setter
    def shocks(self, value: Tuple[MarketDataPatternAndShock, ...]):
        self._property_changed('shocks')
        self.__shocks = value        


class Position(Base):
        
    @camel_case_translate
    def __init__(
        self,
        asset_id: str = None,
        quantity: float = None,
        party_to: SimpleParty = None,
        party_from: SimpleParty = None,
        external_ids: Tuple[dict, ...] = None,
        asset_info: InstrumentBase = None,
        notional: float = None,
        claim_type: Union[ClaimType, str] = None,
        currency: Union[Currency, str] = None,
        counter_party_book_name: str = None,
        description: str = None,
        effective_date: datetime.date = None,
        expiration_date: datetime.date = None,
        external_trade_id: str = None,
        parent_security_type: str = None,
        termination_date: datetime.date = None,
        name: str = None
    ):        
        super().__init__()
        self.asset_id = asset_id
        self.quantity = quantity
        self.party_to = party_to
        self.party_from = party_from
        self.external_ids = external_ids
        self.asset_info = asset_info
        self.notional = notional
        self.claim_type = claim_type
        self.currency = currency
        self.counter_party_book_name = counter_party_book_name
        self.description = description
        self.effective_date = effective_date
        self.expiration_date = expiration_date
        self.external_trade_id = external_trade_id
        self.parent_security_type = parent_security_type
        self.termination_date = termination_date
        self.name = name

    @property
    def asset_id(self) -> str:
        """Marquee unique asset identifier."""
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: str):
        self._property_changed('asset_id')
        self.__asset_id = value        

    @property
    def quantity(self) -> float:
        """Quantity of position"""
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float):
        self._property_changed('quantity')
        self.__quantity = value        

    @property
    def party_to(self) -> SimpleParty:
        return self.__party_to

    @party_to.setter
    def party_to(self, value: SimpleParty):
        self._property_changed('party_to')
        self.__party_to = value        

    @property
    def party_from(self) -> SimpleParty:
        return self.__party_from

    @party_from.setter
    def party_from(self, value: SimpleParty):
        self._property_changed('party_from')
        self.__party_from = value        

    @property
    def external_ids(self) -> Tuple[dict, ...]:
        """A list of identifiers (external to Marquee) for this position"""
        return self.__external_ids

    @external_ids.setter
    def external_ids(self, value: Tuple[dict, ...]):
        self._property_changed('external_ids')
        self.__external_ids = value        

    @property
    def asset_info(self) -> InstrumentBase:
        """Valid Instruments"""
        return self.__asset_info

    @asset_info.setter
    def asset_info(self, value: InstrumentBase):
        self._property_changed('asset_info')
        self.__asset_info = value        

    @property
    def notional(self) -> float:
        """Notional value of the positions."""
        return self.__notional

    @notional.setter
    def notional(self, value: float):
        self._property_changed('notional')
        self.__notional = value        

    @property
    def claim_type(self) -> Union[ClaimType, str]:
        """Claim Type with reference to a position."""
        return self.__claim_type

    @claim_type.setter
    def claim_type(self, value: Union[ClaimType, str]):
        self._property_changed('claim_type')
        self.__claim_type = get_enum_value(ClaimType, value)        

    @property
    def clearing_house(self) -> str:
        """Clearing house for a trade settlement."""
        return 'LCH'        

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self._property_changed('currency')
        self.__currency = get_enum_value(Currency, value)        

    @property
    def counter_party_book_name(self) -> str:
        """Counter Party for a trade or position."""
        return self.__counter_party_book_name

    @counter_party_book_name.setter
    def counter_party_book_name(self, value: str):
        self._property_changed('counter_party_book_name')
        self.__counter_party_book_name = value        

    @property
    def description(self) -> str:
        """Description of a particular trade or position."""
        return self.__description

    @description.setter
    def description(self, value: str):
        self._property_changed('description')
        self.__description = value        

    @property
    def effective_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__effective_date

    @effective_date.setter
    def effective_date(self, value: datetime.date):
        self._property_changed('effective_date')
        self.__effective_date = value        

    @property
    def expiration_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value: datetime.date):
        self._property_changed('expiration_date')
        self.__expiration_date = value        

    @property
    def external_trade_id(self) -> str:
        """External Trade Id for a particular trade."""
        return self.__external_trade_id

    @external_trade_id.setter
    def external_trade_id(self, value: str):
        self._property_changed('external_trade_id')
        self.__external_trade_id = value        

    @property
    def parent_security_type(self) -> str:
        """Security type of the parent trade for a position."""
        return self.__parent_security_type

    @parent_security_type.setter
    def parent_security_type(self, value: str):
        self._property_changed('parent_security_type')
        self.__parent_security_type = value        

    @property
    def termination_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__termination_date

    @termination_date.setter
    def termination_date(self, value: datetime.date):
        self._property_changed('termination_date')
        self.__termination_date = value        


class LiquidityRequest(Base):
        
    """Required parameters in order to get liquidity information on a set of positions"""

    @camel_case_translate
    def __init__(
        self,
        notional: float = None,
        positions: dict = None,
        risk_model: str = None,
        date: datetime.date = None,
        currency: Union[Currency, str] = None,
        participation_rate: float = None,
        execution_horizon: float = None,
        execution_start_time: datetime.datetime = None,
        execution_end_time: datetime.datetime = None,
        benchmark_id: str = None,
        measures: Tuple[Union[LiquidityMeasure, str], ...] = None,
        time_series_benchmark_ids: Tuple[str, ...] = None,
        time_series_start_date: datetime.date = None,
        time_series_end_date: datetime.date = None,
        format_: Union[Format, str] = None,
        report_parameters: LiquidityReportParameters = None,
        name: str = None
    ):        
        super().__init__()
        self.notional = notional
        self.positions = positions
        self.risk_model = risk_model
        self.date = date
        self.currency = currency
        self.participation_rate = participation_rate
        self.execution_horizon = execution_horizon
        self.execution_start_time = execution_start_time
        self.execution_end_time = execution_end_time
        self.benchmark_id = benchmark_id
        self.measures = measures
        self.time_series_benchmark_ids = time_series_benchmark_ids
        self.time_series_start_date = time_series_start_date
        self.time_series_end_date = time_series_end_date
        self.__format = get_enum_value(Format, format_)
        self.report_parameters = report_parameters
        self.name = name

    @property
    def notional(self) -> float:
        """Notional value of the positions."""
        return self.__notional

    @notional.setter
    def notional(self, value: float):
        self._property_changed('notional')
        self.__notional = value        

    @property
    def positions(self) -> dict:
        """A set of quantity or weighted positions."""
        return self.__positions

    @positions.setter
    def positions(self, value: dict):
        self._property_changed('positions')
        self.__positions = value        

    @property
    def risk_model(self) -> str:
        """Marquee unique risk model identifier"""
        return self.__risk_model

    @risk_model.setter
    def risk_model(self, value: str):
        self._property_changed('risk_model')
        self.__risk_model = value        

    @property
    def date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__date

    @date.setter
    def date(self, value: datetime.date):
        self._property_changed('date')
        self.__date = value        

    @property
    def currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self._property_changed('currency')
        self.__currency = get_enum_value(Currency, value)        

    @property
    def participation_rate(self) -> float:
        return self.__participation_rate

    @participation_rate.setter
    def participation_rate(self, value: float):
        self._property_changed('participation_rate')
        self.__participation_rate = value        

    @property
    def execution_horizon(self) -> float:
        return self.__execution_horizon

    @execution_horizon.setter
    def execution_horizon(self, value: float):
        self._property_changed('execution_horizon')
        self.__execution_horizon = value        

    @property
    def execution_start_time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__execution_start_time

    @execution_start_time.setter
    def execution_start_time(self, value: datetime.datetime):
        self._property_changed('execution_start_time')
        self.__execution_start_time = value        

    @property
    def execution_end_time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__execution_end_time

    @execution_end_time.setter
    def execution_end_time(self, value: datetime.datetime):
        self._property_changed('execution_end_time')
        self.__execution_end_time = value        

    @property
    def benchmark_id(self) -> str:
        """Marquee unique asset identifier of the benchmark."""
        return self.__benchmark_id

    @benchmark_id.setter
    def benchmark_id(self, value: str):
        self._property_changed('benchmark_id')
        self.__benchmark_id = value        

    @property
    def measures(self) -> Tuple[Union[LiquidityMeasure, str], ...]:
        return self.__measures

    @measures.setter
    def measures(self, value: Tuple[Union[LiquidityMeasure, str], ...]):
        self._property_changed('measures')
        self.__measures = value        

    @property
    def time_series_benchmark_ids(self) -> Tuple[str, ...]:
        """Marquee unique identifiers of assets to be used as benchmarks."""
        return self.__time_series_benchmark_ids

    @time_series_benchmark_ids.setter
    def time_series_benchmark_ids(self, value: Tuple[str, ...]):
        self._property_changed('time_series_benchmark_ids')
        self.__time_series_benchmark_ids = value        

    @property
    def time_series_start_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__time_series_start_date

    @time_series_start_date.setter
    def time_series_start_date(self, value: datetime.date):
        self._property_changed('time_series_start_date')
        self.__time_series_start_date = value        

    @property
    def time_series_end_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__time_series_end_date

    @time_series_end_date.setter
    def time_series_end_date(self, value: datetime.date):
        self._property_changed('time_series_end_date')
        self.__time_series_end_date = value        

    @property
    def format(self) -> Union[Format, str]:
        """Alternative format for data to be returned in"""
        return self.__format

    @format.setter
    def format(self, value: Union[Format, str]):
        self._property_changed('format')
        self.__format = get_enum_value(Format, value)        

    @property
    def report_parameters(self) -> LiquidityReportParameters:
        """Parameters to be used on liquidity reports"""
        return self.__report_parameters

    @report_parameters.setter
    def report_parameters(self, value: LiquidityReportParameters):
        self._property_changed('report_parameters')
        self.__report_parameters = value        


class MarketDataScenario(Base):
        
    """A market data scenario to apply to the calculation"""

    @camel_case_translate
    def __init__(
        self,
        scenario: Scenario,
        subtract_base: bool = False,
        name: str = None
    ):        
        super().__init__()
        self.scenario = scenario
        self.subtract_base = subtract_base
        self.name = name

    @property
    def scenario(self) -> Scenario:
        """Market data scenarios"""
        return self.__scenario

    @scenario.setter
    def scenario(self, value: Scenario):
        self._property_changed('scenario')
        self.__scenario = value        

    @property
    def subtract_base(self) -> bool:
        """Subtract values computed under the base market data state, to return a diff, if
           true"""
        return self.__subtract_base

    @subtract_base.setter
    def subtract_base(self, value: bool):
        self._property_changed('subtract_base')
        self.__subtract_base = value        


class PositionSet(Base):
        
    @camel_case_translate
    def __init__(
        self,
        id_: str = None,
        position_date: datetime.date = None,
        last_update_time: datetime.datetime = None,
        positions: Tuple[Position, ...] = None,
        type_: str = None,
        divisor: float = None,
        last_updated_time: datetime.datetime = None,
        name: str = None
    ):        
        super().__init__()
        self.__id = id_
        self.position_date = position_date
        self.last_update_time = last_update_time
        self.positions = positions
        self.__type = type_
        self.divisor = divisor
        self.last_updated_time = last_updated_time
        self.name = name

    @property
    def id(self) -> str:
        """Unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def position_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__position_date

    @position_date.setter
    def position_date(self, value: datetime.date):
        self._property_changed('position_date')
        self.__position_date = value        

    @property
    def last_update_time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__last_update_time

    @last_update_time.setter
    def last_update_time(self, value: datetime.datetime):
        self._property_changed('last_update_time')
        self.__last_update_time = value        

    @property
    def positions(self) -> Tuple[Position, ...]:
        """Array of quantity position objects."""
        return self.__positions

    @positions.setter
    def positions(self, value: Tuple[Position, ...]):
        self._property_changed('positions')
        self.__positions = value        

    @property
    def type(self) -> str:
        """The composition type of a Portfolio"""
        return self.__type

    @type.setter
    def type(self, value: str):
        self._property_changed('type')
        self.__type = value        

    @property
    def divisor(self) -> float:
        """optional index divisor for a position set"""
        return self.__divisor

    @divisor.setter
    def divisor(self, value: float):
        self._property_changed('divisor')
        self.__divisor = value        

    @property
    def last_updated_time(self) -> datetime.datetime:
        """Timestamp of when the object was last updated"""
        return self.__last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, value: datetime.datetime):
        self._property_changed('last_updated_time')
        self.__last_updated_time = value        


class RiskPosition(Base):
        
    @camel_case_translate
    def __init__(
        self,
        instrument: Priceable,
        quantity: float = None,
        name: str = None
    ):        
        super().__init__()
        self.instrument = instrument
        self.quantity = quantity
        self.name = name

    @property
    def instrument(self) -> Priceable:
        """Instrument or Id   To specify a Marquee asset use the asset Id. For listed
           products use an XRef, e.g. { 'bid': 'NGZ19 Comdty' }, { 'isin':
           'US912810SD19' }. To specify an instrument use one of the listed
           types"""
        return self.__instrument

    @instrument.setter
    def instrument(self, value: Priceable):
        self._property_changed('instrument')
        self.__instrument = value        

    @property
    def quantity(self) -> float:
        """Quantity of instrument"""
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float):
        self._property_changed('quantity')
        self.__quantity = value        


class RiskRequest(Base):
        
    """Object representation of a risk calculation request"""

    @camel_case_translate
    def __init__(
        self,
        positions: Tuple[RiskPosition, ...],
        measures: Tuple[RiskMeasure, ...],
        pricing_and_market_data_as_of: Tuple[PricingDateAndMarketDataAsOf, ...] = None,
        pricing_location: Union[PricingLocation, str] = 'NYC',
        market_data_vendor: Union[MarketDataVendor, str] = 'Goldman Sachs',
        wait_for_results: bool = False,
        scenario: MarketDataScenario = None,
        report_id: str = None,
        data_set_field_maps: Tuple[DataSetFieldMap, ...] = None,
        parameters: RiskRequestParameters = None,
        request_visible_to_gs: bool = False,
        name: str = None
    ):        
        super().__init__()
        self.positions = positions
        self.measures = measures
        self.pricing_and_market_data_as_of = pricing_and_market_data_as_of
        self.pricing_location = pricing_location
        self.market_data_vendor = market_data_vendor
        self.wait_for_results = wait_for_results
        self.scenario = scenario
        self.report_id = report_id
        self.data_set_field_maps = data_set_field_maps
        self.parameters = parameters
        self.request_visible_to_gs = request_visible_to_gs
        self.name = name

    @property
    def positions(self) -> Tuple[RiskPosition, ...]:
        """The positions on which to run the risk calculation"""
        return self.__positions

    @positions.setter
    def positions(self, value: Tuple[RiskPosition, ...]):
        self._property_changed('positions')
        self.__positions = value        

    @property
    def measures(self) -> Tuple[RiskMeasure, ...]:
        """A collection of risk measures to compute. E.g. { 'measureType': 'Delta',
           'assetClass': 'Equity'"""
        return self.__measures

    @measures.setter
    def measures(self, value: Tuple[RiskMeasure, ...]):
        self._property_changed('measures')
        self.__measures = value        

    @property
    def pricing_and_market_data_as_of(self) -> Tuple[PricingDateAndMarketDataAsOf, ...]:
        """Pricing date and market data as of (date or time)"""
        return self.__pricing_and_market_data_as_of

    @pricing_and_market_data_as_of.setter
    def pricing_and_market_data_as_of(self, value: Tuple[PricingDateAndMarketDataAsOf, ...]):
        self._property_changed('pricing_and_market_data_as_of')
        self.__pricing_and_market_data_as_of = value        

    @property
    def pricing_location(self) -> Union[PricingLocation, str]:
        """The location for pricing and market data"""
        return self.__pricing_location

    @pricing_location.setter
    def pricing_location(self, value: Union[PricingLocation, str]):
        self._property_changed('pricing_location')
        self.__pricing_location = get_enum_value(PricingLocation, value)        

    @property
    def market_data_vendor(self) -> Union[MarketDataVendor, str]:
        """The market data provider"""
        return self.__market_data_vendor

    @market_data_vendor.setter
    def market_data_vendor(self, value: Union[MarketDataVendor, str]):
        self._property_changed('market_data_vendor')
        self.__market_data_vendor = get_enum_value(MarketDataVendor, value)        

    @property
    def wait_for_results(self) -> bool:
        """For short-running requests this may be set to true and the results will be
           returned directly. If false, the response will contain the Id to
           retrieve the results"""
        return self.__wait_for_results

    @wait_for_results.setter
    def wait_for_results(self, value: bool):
        self._property_changed('wait_for_results')
        self.__wait_for_results = value        

    @property
    def scenario(self) -> MarketDataScenario:
        """A market data scenario to apply to the calculation"""
        return self.__scenario

    @scenario.setter
    def scenario(self, value: MarketDataScenario):
        self._property_changed('scenario')
        self.__scenario = value        

    @property
    def report_id(self) -> str:
        """Marquee unique identifier"""
        return self.__report_id

    @report_id.setter
    def report_id(self, value: str):
        self._property_changed('report_id')
        self.__report_id = value        

    @property
    def data_set_field_maps(self) -> Tuple[DataSetFieldMap, ...]:
        """A mapping list between risk measure types and data set fields"""
        return self.__data_set_field_maps

    @data_set_field_maps.setter
    def data_set_field_maps(self, value: Tuple[DataSetFieldMap, ...]):
        self._property_changed('data_set_field_maps')
        self.__data_set_field_maps = value        

    @property
    def parameters(self) -> RiskRequestParameters:
        """Parameters for the risk request"""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: RiskRequestParameters):
        self._property_changed('parameters')
        self.__parameters = value        

    @property
    def request_visible_to_gs(self) -> bool:
        return self.__request_visible_to_gs

    @request_visible_to_gs.setter
    def request_visible_to_gs(self, value: bool):
        self._property_changed('request_visible_to_gs')
        self.__request_visible_to_gs = value        
