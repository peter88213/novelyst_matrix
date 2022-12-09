[Project homepage](https://peter88213.github.io/novelyst_matrix)

--- 

A simple [novelyst](https://peter88213.github.io/novelyst/) plugin providing a book/series matrix manager. 
.

### Installation

If [novelyst](https://peter88213.github.io/novelyst/) is installed, the setup script auto-installs the *novelyst_matrix* plugin in the *novelyst* plugin directory.

The plugin adds an "Edit" entry to the *novelyst* "Scene" menu. 


#### Open a matrix

- By default, the latest matrix selected is preset. You can change it with **File > Open**.

#### Create a new matrix

- You can create a new matrix with **File > New**. This will close the current matrix
  and open a file dialog asking for the location and file name of the matrix to create.
- Once you specified a valid file path, a blank matrix appears.

#### Create a new series

- You can add a new series with **Series > Add**. Edit the series' title and description in the right window.

#### Add books to the matrix

- You can add the current novelyst project as a book to the matrix. Use **Book > Add current project to matrix**.
- If a series is selected, the book is added as a part of this series.

#### Update book description

- You can update the book description from the current project. Use **Book > Update book data from current project**. 
  Be sure not to change the book title, because it is used as identifier. 

#### Remove books from the matrix

- You can remove the selected book from the matrix. Use **Book > Remove selected book from the matrix**.

#### Move series and books

Drag and drop while pressing the **Alt** key. Be aware, there is no "Undo" feature. 

#### Remove books

Either select item and hit the **Del** key, or use **Book > Remove selected book from the matrix**.

- When removing a book from the matrix, the project file associated is kept on disc. 

#### Delete a series

Either select series and hit the **Del** key, or use **Series > Remove selected series but keep the books**.

- When deleting a matrix, the books are kept by default.
- Use **Series > Remove selected series** to delete the selected series and remove all its books from the matrix. 

### Exit 

- You can exit via **File > Exit**, or with **Ctrl-Q**.
- When exiting the program, you will be asked for applying changes.


## License

This is Open Source software, and the *novelyst_matrix* plugin is licenced under GPLv3. See the
[GNU General Public License website](https://www.gnu.org/licenses/gpl-3.0.en.html) for more
details, or consult the [LICENSE](https://github.com/peter88213/novelyst_matrix/blob/main/LICENSE) file.
