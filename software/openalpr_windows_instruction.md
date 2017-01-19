1. Use [https://github.com/peters/openalpr-windows](https://github.com/peters/openalpr-windows)
2. Make sure there is cmake make git
3. Use git shell to do following commands
```
git clone https://github.com/openalpr/openalpr.git
cd openalpr
git clone --recursive https://github.com/peters/openalpr-windows.git windows
cd windows
git submodule update --init --recursive
```
4. Comment out in build.ps1 `#Copy-Item $OpenALPROutputDir\statedetection\$Configuration\statedetection.lib -Force $DestinationDir\statedetection.lib | Out-Null`
5. Comment out in build.ps1 `#Build-OpenALPRNet	`
6. Add to build.ps1
```
`Vcxproj-Set $VcxProjectFilename '/rs:Project/rs:PropertyGroup[@Label="Globals"]/rs:OpenALPRVersion' $OpenALPRVersion
        Vcxproj-Set $VcxProjectFilename '/rs:Project/rs:PropertyGroup[@Label="Globals"]/rs:TesseractVersion' $TesseractVersion`
```
7. Do [bottom few steps for GO binding](https://github.com/peters/openalpr-windows/issues/3) (I think its optional if remove from CMakeLists?)
8. In openalpr/src CMakeLists.txt remove if around `add_subdirectory(bindings/python)` and comment out `C binding`