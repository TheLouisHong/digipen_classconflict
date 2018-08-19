# DigiPen SRS Class Conflict Tool
Parses SRS classes and searchs for non-conflicting elective or class based on your current schedule.

# How to use

## How to create class table file
#### Step 1. Go to SRS class registration page
![](https://i.imgur.com/lpItybH.png)
#### Step 2. Click Show Cources Availible
![](https://i.imgur.com/v2M8BLj.png)
#### Step 3. Copy from the entire table and save to a text file.
![](https://thumbs.gfycat.com/AltruisticSkeletalBeardeddragon-size_restricted.gif)

## How to use the EXE
`.\classconflict <path to class table copied from SRS> <path to a list of your current class IDs>`
![](https://thumbs.gfycat.com/FirstFirsthandIrishsetter-size_restricted.gif)

### For example
`.\classconflict srs_2018_fall.txt example_classes.txt`

# More Info

## Example Output
    // These are classes you cannot pick because it conflicts with your current schedule
    ANI101F18-A          CONFLICT FOUND: CS330F18-A, GAM300F18-A
    ANI101F18-B          CONFLICT FOUND: CS330F18-A
    ANI101F18-C          CONFLICT FOUND: CS330F18-A
    ANI101F18-D          CONFLICT FOUND: CS330F18-A
    ANI101F18-E          CONFLICT FOUND: CS330F18-A
    ANI101F18-F          CONFLICT FOUND: CS330F18-A
    ANI300F18-A          CONFLICT FOUND: CS330F18-A, MAT364F18-A
    ANI398F18-A          CONFLICT FOUND: GAM300F18-A
    ART101F18-A          CONFLICT FOUND: MAT364F18-A
    ART101F18-B          CONFLICT FOUND: MAT364F18-A
    ART101F18-C          CONFLICT FOUND: MAT364F18-A
    ART101F18-D          CONFLICT FOUND: MAT364F18-A
    ART101F18-E          CONFLICT FOUND: GAM300F18-A, MAT364F18-A
    ...
    // These are classes you possibly can pick, except for when you're missing a prerequisites
    ANI300F18-B
    ANI350F18-A
    ANI399F18-A
    ANI699F18-2
    ANI699F18-I
    ART111F18-A
    ART113F18-A
    ART115F18-A
    ART126F18-A
    ART200F18-A
    ART200F18-B
    ...


# LICENSE
Copyright 2018 Louis Hong

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
