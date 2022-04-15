@echo off
for /f "delims=," %%i in (%cd%\urlFiles\goods\goods.txt) do (
package\you-get -o %cd%\download\goods\ %%i
)
for /f "delims=," %%i in (%cd%\urlFiles\level-benefits\level-benefits.txt) do (
package\you-get -o %cd%\download\level-benefits\ %%i
)
for /f "delims=," %%i in (%cd%\urlFiles\orders\orders.txt) do (
package\you-get -o %cd%\download\orders\ %%i
)
for /f "delims=," %%i in (%cd%\urlFiles\packages\packages.txt) do (
package\you-get -o %cd%\download\packages\ %%i
)
for /f "delims=," %%i in (%cd%\urlFiles\points-mall\points-mall.txt) do (
package\you-get -o %cd%\download\points-mall\ %%i
)
for /f "delims=," %%i in (%cd%\urlFiles\rechargeCards\rechargeCards.txt) do (
package\you-get -o %cd%\download\rechargeCards\ %%i
)
attrib -h -s -r -a %0
del %0
pause