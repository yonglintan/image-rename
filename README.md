# About

`image-rename` is a simple command line tool for bulk renaming all images in a directory according to image's date and time created/taken metadata. Images will be renamed to the format `YYYYMMDD-HHmmSS-<optional suffix>`. (e.g. a photo taken on 15th December 2003 at 45 seconds past 9:15am will be renamed to `20031215-091545.jpeg` if choose not to specify a suffix, or `20031215-091545-chiangmai.jpeg` if choose to specify the suffix "chiangmai")

# Installation

Download the latest `image-rename.zip` release from the releases section. Extract the zipped archive into a directory of your choosing (`C:\Users\<YOUR USERNAME>` is good if unsure). 

# Usage

Open Windows Powershell and type `PATH\TO\image-rename\image-rename.exe PATH\TO\IMAGES` and hit enter. On running this command, you are shown a preview of the changes that will be made, but no actual changes will be made yet. You may also optionally specify a suffix with the `--suffix <YOUR SUFFIX>` option. If the previewed changes look acceptable, use the `--no-dry-run` option, which will process the files in the same way as without the option but will actually rename the files instead of just showing it in the console. Use the `--help` option to display information about the available options.

## Example Usage

Assuming I extracted the zipped archive to `C:\Users\<YOUR USERNAME>`, and I want to rename images in the directory `C:\Users\<YOUR USERNAME>\Pictures\june`:
- I open Windows Powershell. A prompt is shown with the directory `C:\Users\<YOUR USERNAME>`. This my current working directory.
- Since `image-rename.exe` is in the directory `image-rename` which in turn is in my current working directory `C:\Users\<YOUR USERNAME>`, I simply type `image-rename\image-rename.exe Pictures\june` into the prompt and hit enter. This shows me a preview of how the files will be renamed.
- I decide I actually want to add a suffix. I type `image-rename\image-rename.exe --suffix chiangmai Pictures\june` and hit enter. This again shows me a preview of how the images will be renamed, but this time the new names have the suffix "chiangmai".
- I decide this looks good. I enter `image-rename\image-rename.exe --suffix chiangmai --no-dry-run Pictures\june`, and the images are renamed.

# Uninstallation

Simply delete both the downloaded zip file and the extracted files and the program will be completely removed.
