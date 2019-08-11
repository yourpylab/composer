from typing import Dict

from composer.aws.efile.filings import EfileFilings
from composer.aws.efile.indices import EfileIndices
from composer.aws.s3 import Bucket, List, file_backed_bucket
import os
from composer.efile.structures.metadata import FilingMetadata

def test_read_efile_indices(fixture_path):
    index_path: str = os.path.join(fixture_path, "efile_indices", "first_timepoint")
    bucket: Bucket = file_backed_bucket(index_path)
    indices: EfileIndices = EfileIndices(bucket)
    expected: List = [
        FilingMetadata(record_id='364201074_201012', irs_efile_id='201101389349300010', irs_dln='93493138000101',
                       ein='364201074', period='201012', name_org='CENTURY WALK CORPORATION', form_type='990',
                       date_submitted='2011-10-12', date_uploaded='2016-03-21T17:23:53',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201101389349300010_public.xml'),
        FilingMetadata(record_id='943041314_201012', irs_efile_id='201102999349300730', irs_dln='93493299007301',
                       ein='943041314', period='201012',
                       name_org='LAW ENFORCEMENT OFFICERS AND FIREFIGHTERS HEALTH AND WELFARE TRUST',
                       form_type='990', date_submitted='2011-11-15', date_uploaded='2016-03-21T17:23:53',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201102999349300730_public.xml'),
        FilingMetadata(record_id='943041314_201012', irs_efile_id='201120919349300412', irs_dln='93493091004121',
                       ein='943041314', period='201012',
                       name_org='LAW ENFORCEMENT OFFICERS AND FIREFIGHTERS HEALTH AND WELFARE TRUST',
                       form_type='990', date_submitted='2011-09-28', date_uploaded='2016-03-21T17:23:53',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201120919349300412_public.xml'),
        FilingMetadata(record_id='208419458_201012', irs_efile_id='201121369349101317', irs_dln='93491136013171',
                       ein='208419458', period='201012', name_org='GROSSHUTTON FAMILY FOUNDATION',
                       form_type='990PF', date_submitted='2011-10-14', date_uploaded='2016-03-21T17:23:53',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201121369349101317_public.xml'),
        FilingMetadata(record_id='260687839_201112', irs_efile_id='201202289349200810', irs_dln='93492228008102',
                       ein='260687839', period='201112', name_org='COOKING WITH KIDS FOUNDATION', form_type='990EZ',
                       date_submitted='2012-10-29', date_uploaded='2016-03-21T17:23:53',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201202289349200810_public.xml'),
        FilingMetadata(record_id='943041314_201112', irs_efile_id='201203049349300935', irs_dln='93493304009352',
                       ein='943041314', period='201112',
                       name_org='LAW ENFORCEMENT OFFICERS AND FIREFIGHTERS HEALTH AND WELFARE TRUST',
                       form_type='990', date_submitted='2012-11-13', date_uploaded='2016-03-21T17:23:53',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201203049349300935_public.xml'),
        FilingMetadata(record_id='208419458_201112', irs_efile_id='201211509349100411', irs_dln='93491150004112',
                       ein='208419458', period='201112', name_org='GROSSHUTTON FAMILY FOUNDATION',
                       form_type='990PF', date_submitted='2012-12-31', date_uploaded='2016-03-21T17:23:53',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201211509349100411_public.xml'),
        FilingMetadata(record_id='943041314_201112', irs_efile_id='201221359349303537', irs_dln='93493135035372',
                       ein='943041314', period='201112',
                       name_org='LAW ENFORCEMENT OFFICERS AND FIREFIGHTERS HEALTH AND WELFARE TRUST',
                       form_type='990', date_submitted='2012-10-11', date_uploaded='2016-03-21T17:23:53',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201221359349303537_public.xml'),
        FilingMetadata(record_id='364201074_201112', irs_efile_id='201240689349300039', irs_dln='93493068000392',
                       ein='364201074', period='201112', name_org='CENTURY WALK CORPORATION CO W BRAND BOBOSKY',
                       form_type='990', date_submitted='2012-09-18', date_uploaded='2016-03-21T17:23:53',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201240689349300039_public.xml'),
        FilingMetadata(record_id='943041314_201212', irs_efile_id='201312909349300041', irs_dln='93493290000413',
                       ein='943041314', period='201212',
                       name_org='LAW ENFORCEMENT OFFICERS AND FIREFIGHTERS HEALTH AND WELFARE TRUST',
                       form_type='990', date_submitted='2014-01-09', date_uploaded='2016-03-21T17:23:53',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201312909349300041_public.xml'),
        FilingMetadata(record_id='943041314_201212', irs_efile_id='201320599349300107', irs_dln='93493059001073',
                       ein='943041314', period='201212',
                       name_org='LAW ENFORCEMENT OFFICERS AND FIREFIGHTERS HEALTH AND WELFARE TRUST',
                       form_type='990', date_submitted='2013-07-17', date_uploaded='2016-03-21T17:23:53',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201320599349300107_public.xml'),
        FilingMetadata(record_id='260687839_201112', irs_efile_id='201322319349200502', irs_dln='93492231005023',
                       ein='260687839', period='201112', name_org='COOKING WITH KIDS FOUNDATION', form_type='990EZ',
                       date_submitted='2013-09-27', date_uploaded='2016-03-21T17:23:53',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201322319349200502_public.xml'),
        FilingMetadata(record_id='364201074_201212', irs_efile_id='201331349349300198', irs_dln='93493134001983',
                       ein='364201074', period='201212', name_org='CENTURY WALK CORPORATION CO W BRAND BOBOSKY',
                       form_type='990', date_submitted='2013-08-14', date_uploaded='2016-03-21T17:23:53',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201331349349300198_public.xml'),
        FilingMetadata(record_id='208419458_201212', irs_efile_id='201331359349102058', irs_dln='93491135020583',
                       ein='208419458', period='201212', name_org='GROSSHUTTON FAMILY FOUNDATION',
                       form_type='990PF', date_submitted='2014-01-13', date_uploaded='2016-03-21T17:23:53',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201331359349102058_public.xml'),
        FilingMetadata(record_id='260687839_201012', irs_efile_id='201332289349200818', irs_dln='93492228008183',
                       ein='260687839', period='201012', name_org='COOKING WITH KIDS FOUNDATION', form_type='990EZ',
                       date_submitted='2013-09-27', date_uploaded='2016-03-21T17:23:53',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201332289349200818_public.xml'),
        FilingMetadata(record_id='260687839_201212', irs_efile_id='201342279349202019', irs_dln='93492227020193',
                       ein='260687839', period='201212', name_org='COOKING WITH KIDS', form_type='990EZ',
                       date_submitted='2013-12-04', date_uploaded='2016-03-21T17:23:53',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201342279349202019_public.xml'),
        FilingMetadata(record_id='943041314_201312', irs_efile_id='201411139349300506', irs_dln='93493113005064',
                       ein='943041314', period='201312',
                       name_org='LAW ENFORCEMENT OFFICERS AND FIREFIGHTERS HEALTH AND WELFARE TRUST',
                       form_type='990', date_submitted='2014-09-24', date_uploaded='2016-03-21T17:23:53',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201411139349300506_public.xml'),
        FilingMetadata(record_id='943041314_201312', irs_efile_id='201413219349304036', irs_dln='93493321040364',
                       ein='943041314', period='201312',
                       name_org='LAW ENFORCEMENT OFFICERS AND FIREFIGHTERS HEALTH AND WELFARE TRUST',
                       form_type='990', date_submitted='2014-12-29', date_uploaded='2016-03-21T17:23:53',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201413219349304036_public.xml'),
        FilingMetadata(record_id='364201074_201312', irs_efile_id='201421349349306507', irs_dln='93493134065074',
                       ein='364201074', period='201312', name_org='CENTURY WALK CORPORATION CO W BRAND BOBOSKY',
                       form_type='990', date_submitted='2014-10-14', date_uploaded='2016-03-21T17:23:53',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201421349349306507_public.xml'),
        FilingMetadata(record_id='260687839_201112', irs_efile_id='201422239349200512', irs_dln='93492223005124',
                       ein='260687839', period='201112', name_org='COOKING WITH KIDS FOUNDATION', form_type='990EZ',
                       date_submitted='2014-10-01', date_uploaded='2016-03-21T17:23:53',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201422239349200512_public.xml'),
        FilingMetadata(record_id='208419458_201312', irs_efile_id='201422309349100612', irs_dln='93491230006124',
                       ein='208419458', period='201312', name_org='GROSSHUTTON FAMILY FOUNDATION',
                       form_type='990PF', date_submitted='2014-10-03', date_uploaded='2016-03-21T17:23:53',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201422309349100612_public.xml'),
        FilingMetadata(record_id='260687839_201312', irs_efile_id='201432239349200108', irs_dln='93492223001084',
                       ein='260687839', period='201312', name_org='COOKING WITH KIDS FOUNDATION', form_type='990EZ',
                       date_submitted='2014-10-21', date_uploaded='2016-03-21T17:23:53',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201432239349200108_public.xml'),
        FilingMetadata(record_id='260687839_201212', irs_efile_id='201432239349200513', irs_dln='93492223005134',
                       ein='260687839', period='201212', name_org='COOKING WITH KIDS', form_type='990EZ',
                       date_submitted='2014-10-20', date_uploaded='2016-03-21T17:23:53',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201432239349200513_public.xml'),
        FilingMetadata(record_id='208419458_201312', irs_efile_id='201441399349100554', irs_dln='93491139005544',
                       ein='208419458', period='201312', name_org='GROSSHUTTON FAMILY FOUNDATION',
                       form_type='990PF', date_submitted='2014-11-07', date_uploaded='2016-03-21T17:23:53',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201441399349100554_public.xml'),
        FilingMetadata(record_id='943041314_201412', irs_efile_id='201520579349300422', irs_dln='93493057004225',
                       ein='943041314', period='201412',
                       name_org='LAW ENFORCEMENT OFFICERS AND FIREFIGHTERS HEALTH AND WELFARE TRUST',
                       form_type='990', date_submitted='2015-07-17', date_uploaded='2016-03-21T17:23:53',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201520579349300422_public.xml'),
        FilingMetadata(record_id='364201074_201412', irs_efile_id='201521949349301272', irs_dln='93493194012725',
                       ein='364201074', period='201412', name_org='CENTURY WALK CORPORATION CO W BRAND BOBOSKY',
                       form_type='990', date_submitted='2015-07-27', date_uploaded='2016-03-21T17:23:53',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201521949349301272_public.xml'),
        FilingMetadata(record_id='208419458_201412', irs_efile_id='201541349349101014', irs_dln='93491134010145',
                       ein='208419458', period='201412', name_org='GROSSHUTTON FAMILY FOUNDATION',
                       form_type='990PF', date_submitted='2015-08-06', date_uploaded='2016-03-21T17:23:53',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201541349349101014_public.xml'),
        FilingMetadata(record_id='260687839_201412', irs_efile_id='201541359349200429', irs_dln='93492135004295',
                       ein='260687839', period='201412', name_org='COOKING WITH KIDS FOUNDATION', form_type='990EZ',
                       date_submitted='2015-08-14', date_uploaded='2016-04-29T13:40:20',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201541359349200429_public.xml'),
        FilingMetadata(record_id='943041314_201412', irs_efile_id='201600639349300035', irs_dln='93493063000356',
                       ein='943041314', period='201412',
                       name_org='LAW ENFORCEMENT OFFICERS AND FIREFIGHTERS HEALTH AND WELFARE TRUST',
                       form_type='990', date_submitted='2016-07-21', date_uploaded='2016-09-09T23:14:27',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201600639349300035_public.xml'),
        FilingMetadata(record_id='260687839_201512', irs_efile_id='201601309349200540', irs_dln='93492130005406',
                       ein='260687839', period='201512', name_org='COOKING WITH KIDS FOUNDATION', form_type='990EZ',
                       date_submitted='2016-09-06', date_uploaded='2016-10-12T19:43:10',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201601309349200540_public.xml'),
        FilingMetadata(record_id='364201074_201512', irs_efile_id='201621379349301212', irs_dln='93493137012126',
                       ein='364201074', period='201512', name_org='CENTURY WALK CORPORATION CO W BRAND BOBOSKY',
                       form_type='990', date_submitted='2016-12-27', date_uploaded='2017-01-11T22:15:19.5060064Z',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201621379349301212_public.xml'),
        FilingMetadata(record_id='943041314_201512', irs_efile_id='201640639349300634', irs_dln='93493063006346',
                       ein='943041314', period='201512',
                       name_org='LAW ENFORCEMENT OFFICERS AND FIREFIGHTERS HEALTH AND WELFARE TRUST',
                       form_type='990', date_submitted='2016-08-16', date_uploaded='2016-09-09T23:14:27',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201640639349300634_public.xml'),
        FilingMetadata(record_id='208419458_201512', irs_efile_id='201642429349100559', irs_dln='93491242005596',
                       ein='208419458', period='201512', name_org='GROSSHUTTON FAMILY FOUNDATION',
                       form_type='990PF', date_submitted='2017-01-05', date_uploaded='2017-01-11T22:15:15',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201642429349100559_public.xml'),
        FilingMetadata(record_id='260687839_201612', irs_efile_id='201702429349200215', irs_dln='93492242002157',
                       ein='260687839', period='201612', name_org='COOKING WITH KIDS FOUNDATION', form_type='990EZ',
                       date_submitted='2017-10-13', date_uploaded='2017-11-15T14:51:02',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201702429349200215_public.xml'),
        FilingMetadata(record_id='943041314_201612', irs_efile_id='201710309349300846', irs_dln='93493030008467',
                       ein='943041314', period='201612',
                       name_org='LAW ENFORCEMENT OFFICERS AND FIREFIGHTERS HEALTH AND WELFARE TRUST',
                       form_type='990', date_submitted='2017-08-03', date_uploaded='2017-09-13T21:58:58',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201710309349300846_public.xml'),
        FilingMetadata(record_id='208419458_201612', irs_efile_id='201721359349103242', irs_dln='93491135032427',
                       ein='208419458', period='201612', name_org='GROSSHUTTON FAMILY FOUNDATION',
                       form_type='990PF', date_submitted='2017-09-26', date_uploaded='2017-10-13T18:40:16',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201721359349103242_public.xml'),
        FilingMetadata(record_id='943041314_201512', irs_efile_id='201730249349300103', irs_dln='93493024001037',
                       ein='943041314', period='201512',
                       name_org='LAW ENFORCEMENT OFFICERS AND FIREFIGHTERS HEALTH AND WELFARE TRUST',
                       form_type='990', date_submitted='2017-07-18', date_uploaded='2017-09-13T21:58:58',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201730249349300103_public.xml'),
        FilingMetadata(record_id='943041314_201412', irs_efile_id='201730249349300543', irs_dln='93493024005437',
                       ein='943041314', period='201412',
                       name_org='LAW ENFORCEMENT OFFICERS AND FIREFIGHTERS HEALTH AND WELFARE TRUST',
                       form_type='990', date_submitted='2017-07-18', date_uploaded='2017-09-13T21:58:58',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201730249349300543_public.xml'),
        FilingMetadata(record_id='364201074_201612', irs_efile_id='201742349349300959', irs_dln='93493234009597',
                       ein='364201074', period='201612', name_org='CENTURY WALK CORPORATION', form_type='990',
                       date_submitted='2017-10-13', date_uploaded='2017-11-15T14:51:02',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201742349349300959_public.xml'),
        FilingMetadata(record_id='943041314_201712', irs_efile_id='201820589349300227', irs_dln='93493058002278',
                       ein='943041314', period='201712',
                       name_org='LAW ENFORCEMENT OFFICERS AND FIREFIGHTERS HEALTH AND WELFARE TRUST',
                       form_type='990', date_submitted='2018-08-02', date_uploaded='2018-10-16T15:38:26',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201820589349300227_public.xml'),
        FilingMetadata(record_id='364201074_201712', irs_efile_id='201842359349300914', irs_dln='93493235009148',
                       ein='364201074', period='201712', name_org='CENTURY WALK CORPORATION', form_type='990',
                       date_submitted='2018-10-19', date_uploaded='2018-11-15T17:06:31',
                       date_downloaded='the current time',
                       url='https://s3.amazonaws.com/irs-form-990/201842359349300914_public.xml')
    ]
    actual: List = sorted(indices, key=lambda filing: filing.irs_efile_id)
    for a in actual:
        a.date_downloaded = 'the current time'
    assert expected == actual

def test_get_efile(fixture_path):
    filings_path: str = os.path.join(fixture_path, "efile_xml")
    bucket: Bucket = file_backed_bucket(filings_path)
    filings: EfileFilings = EfileFilings(bucket)
    expected: Dict = {
        "Return": {
            "ReturnHeader": {
                "Filer": {
                    "Name": {
                        "BusinessNameLine1": "Cooking With Kids Foundation"
                    },
                    "USAddress": {
                        "AddressLine1": "1571 Ptarmigan Drive 1A",
                        "City": "Walnut Creek",
                        "State": "CA",
                        "ZIPCode": "945955315"
                    },
                    "EIN": "260687839",
                    "NameControl": "COOK",
                    "Phone": "9259321114"
                },
                "Officer": {
                    "Name": "Stephen Smith",
                    "Title": "CFO",
                    "Phone": "9255133015",
                    "DateSigned": "2013-08-16"
                },
                "Timestamp": "2013-08-16T17:23:00-07:00",
                "TaxPeriodEndDate": "2010-12-31",
                "ReturnType": "990EZ",
                "TaxPeriodBeginDate": "2010-01-01",
                "TaxYear": "2010",
                "BuildTS": "2016-02-24 21:20:13Z"
            },
            "ReturnData": {
                "IRS990EZ": {
                    "CashSavingsAndInvestments": {
                        "BOY": "0",
                        "EOY": "0"
                    },
                    "LandAndBuildings": {
                        "BOY": "0",
                        "EOY": "0"
                    },
                    "OtherAssetsTotal": {
                        "BOY": "0",
                        "EOY": "0"
                    },
                    "TotalAssets": {
                        "BOY": "0",
                        "EOY": "0"
                    },
                    "SumOfTotalLiabilities": {
                        "BOY": "3792",
                        "EOY": "3792"
                    },
                    "NetAssetsOrFundBalances": {
                        "BOY": "-3792",
                        "EOY": "-3792"
                    },
                    "ProgramServiceAccomplishment": {
                        "DescriptionProgramServiceAccom": "Foundation was primarily engaged in organizational activities",
                        "GrantsAndAllocations": "0",
                        "ProgramServiceExpenses": "0"
                    },
                    "OfficerDirectorTrusteeKeyEmpl": [
                        {
                            "AddressUS": {
                                "AddressLine1": "1571 Ptarmigan Drive 1A",
                                "City": "Walnut Creek",
                                "State": "CA",
                                "ZIPCode": "945955315"
                            },
                            "PersonName": "Linda Kay Rexroat",
                            "Title": "President, CEO, and Director",
                            "AvgHoursPerWkDevotedToPosition": "40",
                            "Compensation": "0",
                            "ContriToEmplBenefitPlansEtc": "0",
                            "ExpenseAccountOtherAllowances": "0"
                        },
                        {
                            "AddressUS": {
                                "AddressLine1": "1571 Ptarmigan Drive 1A",
                                "City": "Walnut Creek",
                                "State": "CA",
                                "ZIPCode": "945955315"
                            },
                            "PersonName": "John Rexroat",
                            "Title": "Secretary and Director",
                            "AvgHoursPerWkDevotedToPosition": "10",
                            "Compensation": "0",
                            "ContriToEmplBenefitPlansEtc": "0",
                            "ExpenseAccountOtherAllowances": "0"
                        },
                        {
                            "AddressUS": {
                                "AddressLine1": "1483 Bismarck Lane",
                                "City": "Brentwood",
                                "State": "CA",
                                "ZIPCode": "945136917"
                            },
                            "PersonName": "Stephen F Smith",
                            "Title": "CFO and Director",
                            "AvgHoursPerWkDevotedToPosition": "2",
                            "Compensation": "0",
                            "ContriToEmplBenefitPlansEtc": "0",
                            "ExpenseAccountOtherAllowances": "0"
                        },
                        {
                            "AddressUS": {
                                "AddressLine1": "1748 Oakmont Drive",
                                "City": "Walnut Creek",
                                "State": "CA",
                                "ZIPCode": "945952012"
                            },
                            "PersonName": "Lou Ann Berardi",
                            "Title": "Director",
                            "AvgHoursPerWkDevotedToPosition": "4",
                            "Compensation": "0",
                            "ContriToEmplBenefitPlansEtc": "0",
                            "ExpenseAccountOtherAllowances": "0"
                        }
                    ],
                    "TheBooksAreInCareOf": {
                        "AddressUS": {
                            "AddressLine1": "1571 Ptarmigan Drive 1A",
                            "City": "Walnut Creek",
                            "State": "CA",
                            "ZIPCode": "945955315"
                        },
                        "NamePerson": "John Rexroat",
                        "TelephoneNumber": "9253236915"
                    },
                    "AmendedReturn": "X",
                    "MethodOfAccountingCash": "X",
                    "ScheduleBNotRequired": "X",
                    "Organization501c3@referenceDocumentId": "R000002",
                    "Organization501c3": "X",
                    "GrossReceipts": "2652",
                    "InfoInScheduleOPartI": "X",
                    "ContributionsGiftsGrantsEtc": "100",
                    "ProgramServiceRevenue": "2552",
                    "MembershipDues": "0",
                    "InvestmentIncome": "0",
                    "GrossAmountFromSaleOfAssets": "0",
                    "CostOtherBasisAndSalesExpenses": "0",
                    "GainOrLossFromSaleOfAssets": "0",
                    "GamingGrossIncome": "0",
                    "FundraisingGrossIncome@contributionsReportedOnLine1a": "0",
                    "FundraisingGrossIncome": "0",
                    "SpecialEventsDirectExpenses": "0",
                    "SpecialEventsNetIncomeLoss": "0",
                    "GrossSalesOfInventory": "0",
                    "CostOfGoodsSold": "0",
                    "GroProfitLossSalesOfInventory": "0",
                    "OtherRevenueTotal": "0",
                    "TotalRevenue": "2652",
                    "GrantsAndSimilarAmountsPaid": "0",
                    "BenefitsPaidToOrForMembers": "0",
                    "SalariesOtherCompEmplBenefits": "24",
                    "FeesAndOthPymtToIndContractors": "20",
                    "OccupancyRentUtilitiesAndMaint": "0",
                    "PrintingPublicationsPostage": "44",
                    "OtherExpensesTotal": "1390",
                    "TotalExpenses": "1478",
                    "ExcessOrDeficitForYear": "1174",
                    "NetAssetsOrFundBalancesBOY": "-3792",
                    "OtherChangesInNetAssets": "-1174",
                    "NetAssetsOrFundBalancesEOY": "-3792",
                    "InfoInScheduleOPartII": "X",
                    "PrimaryExemptPurpose": "Promote healthy eating thru Cooking With Kids classes",
                    "TotalProgramServiceExpenses": "0",
                    "ActivitiesNotPreviouslyRpt": "0",
                    "MadeChangesToOrgnzngEtcDoc": "0",
                    "OrganizationHadUBI": "0",
                    "OrganizationDissolvedEtc": "0",
                    "DirectIndirectPoliticalExpend": "0",
                    "DidOrgFileForm1120POLThisYear": "0",
                    "MadeLoansToFromOfficers": "1",
                    "LoansToFromOfficers@referenceDocumentId": "R000003",
                    "LoansToFromOfficers": "3792",
                    "TaxImposedUnderIRC4911": "0",
                    "TaxImposedUnderIRC4912": "0",
                    "TaxImposedUnderIRC4955": "0",
                    "EngagedInExcessBenefitTrans@referenceDocumentId": "R000003",
                    "EngagedInExcessBenefitTrans": "0",
                    "AmountOfTaxImposedOnOrgMgr": "0",
                    "AmountOfTaxReimbursedByOrg": "0",
                    "ProhibitedTaxShelterTrans": "0",
                    "StatesWhereCopyOfReturnIsFiled": "CA",
                    "ForeignFinancialAccount": "0",
                    "ForeignOffice": "0",
                    "MaintainAnyDonorAdvisedFunds": "0",
                    "DoesOrgHaveHospital": "0",
                    "TanningServicesProvided": "0",
                    "RelatedOrgControlledEntity": "0",
                    "EngagePoliticalCmpgnActivities": "0",
                    "EngageInLobbyingActivities": "0",
                    "OperatingSchool": "0",
                    "TrnsfrsExemptNonCharRelatedOrg": "0",
                    "PartVIOfCompOfHighestPaidEmpl": "NONE",
                    "PartVIAHghstPaidCntrctProfSer": "NONE",
                    "FiledScheduleA": "1"
                },
                "IRS990ScheduleA": {
                    "GiftsGrantsContribReceived509": {
                        "CurrentTaxYear": "100",
                        "Total": "100"
                    },
                    "GrossReceiptsFromAdmissions": {
                        "CurrentTaxYear": "0",
                        "Total": "0"
                    },
                    "GrossReceiptsFromNonUBI": {
                        "CurrentTaxYear": "0",
                        "Total": "0"
                    },
                    "TaxRevLeviedForOrgBenefit509": {
                        "CurrentTaxYear": "0",
                        "Total": "0"
                    },
                    "ValueOfSvcsFcltsFurnishdByGovt": {
                        "CurrentTaxYear": "0",
                        "Total": "0"
                    },
                    "Total509": {
                        "CurrentTaxYearMinus4Years": "0",
                        "CurrentTaxYearMinus3Years": "0",
                        "CurrentTaxYearMinus2Years": "0",
                        "CurrentTaxYearMinus1Year": "0",
                        "CurrentTaxYear": "100",
                        "Total": "100"
                    },
                    "AmtsRecdFromDisqualPersons": {
                        "CurrentTaxYear": "0",
                        "Total": "0"
                    },
                    "AmtsFromSubstContributors": {
                        "CurrentTaxYear": "0",
                        "Total": "0"
                    },
                    "SupportFromDQPsEtc": {
                        "CurrentTaxYearMinus4Years": "0",
                        "CurrentTaxYearMinus3Years": "0",
                        "CurrentTaxYearMinus2Years": "0",
                        "CurrentTaxYearMinus1Year": "0",
                        "CurrentTaxYear": "0",
                        "Total": "0"
                    },
                    "GrossInvestmentIncome509": {
                        "CurrentTaxYear": "0",
                        "Total": "0"
                    },
                    "Post1975UBTI": {
                        "CurrentTaxYear": "0",
                        "Total": "0"
                    },
                    "InvestmentIncomeAndUBTI": {
                        "CurrentTaxYearMinus4Years": "0",
                        "CurrentTaxYearMinus3Years": "0",
                        "CurrentTaxYearMinus2Years": "0",
                        "CurrentTaxYearMinus1Year": "0",
                        "CurrentTaxYear": "0",
                        "Total": "0"
                    },
                    "NetIncomeFromOtherUBI": {
                        "CurrentTaxYear": "0",
                        "Total": "0"
                    },
                    "OtherIncome509": {
                        "CurrentTaxYear": "0",
                        "Total": "0"
                    },
                    "TotalSupportTotal": {
                        "CurrentTaxYearMinus4Years": "0",
                        "CurrentTaxYearMinus3Years": "0",
                        "CurrentTaxYearMinus2Years": "0",
                        "CurrentTaxYearMinus1Year": "0",
                        "CurrentTaxYear": "100",
                        "Total": "100"
                    },
                    "PubliclySupportedOrg509a2": "X",
                    "PublicSupportTotal509": "100",
                    "First5Years509": "X"
                },
                "IRS990ScheduleL": {
                    "LoanTable": {
                        "NamePerson": "Linda Kay Rexroat",
                        "PurposeOfLoan": "Startup Expenses incurred in 2009",
                        "LoanToOrganization": "X",
                        "OriginalPrincipalAmount": "3792",
                        "BalanceDue": "3792",
                        "Default": "0",
                        "ApprovedByBoard": "0",
                        "WrittenAgreement": "0"
                    },
                    "TotalBalanceDue": "3792"
                },
                "IRS990ScheduleO": {
                    "GeneralExplanation": [
                        {
                            "Identifier": "F99Z_P00_S00_L0B",
                            "ReturnReference": "Form 990-EZ, Header, Line B",
                            "Explanation": "To reconcile with separate books established for Foundation subsequent to 2010 and account for startup funding from Executive Director"
                        },
                        {
                            "Identifier": "F99Z_P01_S00_L16",
                            "ReturnReference": "Form 990-EZ, Part I, Line 16",
                            "Explanation": "Description;Amount^Foundation Meeting Expenses;716|Key Person Insurance;397|Promotions and Marketing;257|Web Site Expenses;20^Total;1390^"
                        },
                        {
                            "Identifier": "F99Z_P01_S00_L20",
                            "ReturnReference": "Form 990-EZ, Part I, Line 20",
                            "Explanation": "To account for fact that Foundation did not have separate checking account at end of 2010"
                        },
                        {
                            "Identifier": "F99Z_P02_S00_L26",
                            "ReturnReference": "Form 990-EZ, Part II, Line 26",
                            "Explanation": "Description;EOY Amount^Loan From Executive Director for Startup Expenses;3792^Total;3792^"
                        }
                    ]
                },
                "ReasonableCauseExplanation": {
                    "Explanation": "This is an Amended filing for a previous return filed timely"
                },
                "IRS990EZ@documentId": "R000001",
                "IRS990EZ@referenceDocumentId": "R000004 R000005",
                "IRS990EZ@softwareId": "10000077",
                "IRS990EZ@softwareVersion": "v1.00",
                "IRS990ScheduleA@documentId": "R000002",
                "IRS990ScheduleA@softwareId": "10000077",
                "IRS990ScheduleA@softwareVersion": "v1.00",
                "IRS990ScheduleL@documentId": "R000003",
                "IRS990ScheduleL@softwareId": "10000077",
                "IRS990ScheduleL@softwareVersion": "v1.00",
                "IRS990ScheduleO@documentId": "R000004",
                "IRS990ScheduleO@softwareId": "10000077",
                "IRS990ScheduleO@softwareVersion": "v1.00",
                "ReasonableCauseExplanation@documentId": "R000005",
                "ReasonableCauseExplanation@softwareId": "10000077",
                "ReasonableCauseExplanation@softwareVersion": "v1.00"
            },
            "ReturnHeader@binaryAttachmentCount": "0",
            "ReturnData@documentCount": "5"
        },
        "Return@returnVersion": "2010v3.4"
    }
    actual: Dict = filings["201332289349200818"]
    assert actual == expected
