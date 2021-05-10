## Validation

### HTML

The [W3C Markup Validator](https://validator.w3.org/#validate_by_input) service was used to validate the HTML code of this project.

- add_hike.html template errors:

    - Bad value for attribute action on element form: Must be non-empty. This error was resolved by completing the action attribute: 

        ``` html 
        action = "{{ url_for('add_hike') }}"
        ``` 
    - The input type number is not allowed the attributes minlength and maxlength. This error was resolved by removing these attributes.

    - Bad value true for attribute readonly on element input. This was resolved by changing the readonly attribute value to "readonly":

        ``` html 
        readonly="readonly"
        ``` 
    - The value of the for attribute of the label element must be the ID of a non-hidden form control. Resolved by changing the value of the for attribute to "picker":

        ``` html 
        <label for="picker">Date:</label>
        ``` 

### CSS

The [W3C CSS Validator](https://jigsaw.w3.org/css-validator/#validate_by_input) service was used to validate the CSS code.

- 2 errors were found. These errors occured because the custom light-green and green variables were used in the linear-gradient function. This seems to be a quirk of the W3C CSS validator as discussed [here](https://stackoverflow.com/questions/64754909/css-validator-error-value-error-background-100-is-not-a-color-stop-value) on stackoverflow. A solution would be to replace the custom variables with the original hex values but I decided to leave the code as is, to make it easier to read and maintain.

- A total of 29 warnings were found. 

    - 1 warning related to the imported Google Fonts style sheet which can be safely ignored.
    - 5 of the warnings related to the custom colour variables which can be safely ignored.
    - 23 of the warnings related to the vendor prefixes. These prefixes are not within the W3C specification and can be safely ignored.
    
![Image](images/css_validator.png)

