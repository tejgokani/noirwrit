# Data sources

All texts come from Project Gutenberg (gutenberg.org), which hosts works it has cleared as public domain in the United States.
Noirwrit applies a stricter rule on top: the work must be published in 1930 or earlier. A title is kept only when one of these holds:

1. Every listed contributor (author, translator, editor) died in 1930 or earlier.
2. The first publication year is well established and is 1930 or earlier (listed in `noirwrit/corpus/catalog.py`, `KNOWN_YEARS`).
3. A pulp issue date in the title is 1930 or earlier.
4. The book's own front matter carries a copyright or publication year, and the latest one is 1930 or earlier.

Any book whose front matter mentions a year after 1930 is left out, even when another rule passes. Unsure means out.

Kept: 263 books. Dropped: 198 (reasons in `data/dropped.jsonl`).

## general (185 books)

| Gutenberg ID | Author | Title | Year | PD basis |
|---|---|---|---|---|
| 1757 | Aldrich, Thomas Bailey | The Cruise of the Dolphin |  | all contributors died by 1907 |
| 293 | Alger, Horatio, Jr. | Paul Prescott's Charge |  | all contributors died by 1899 |
| 296 | Alger, Horatio, Jr. | The Cash Boy |  | all contributors died by 1899 |
| 1078 | Altsheler, Joseph A. (Joseph Alexander) | The Scouts of the Valley |  | all contributors died by 1919 |
| 615 | Ariosto, Lodovico | Orlando Furioso |  | all contributors died by 1843 |
| 1607 | Astor, John Jacob | A Journey in Other Worlds: A Romance of the Future |  | all contributors died by 1912 |
| 121 | Austen, Jane | Northanger Abbey |  | all contributors died by 1817 |
| 783 | Badger, Jos. E. (Joseph Edward) | The Lost City |  | all contributors died by 1909 |
| 646 | Ballantyne, R. M. (Robert Michael) | The Coral Island: A Tale of the Pacific Ocean |  | all contributors died by 1894 |
| 1456 | Balzac, Honoré de | An Episode under the Terror |  | all contributors died by 1927 |
| 1454 | Balzac, Honoré de | Maitre Cornelius |  | all contributors died by 1908 |
| 1569 | Balzac, Honoré de | The Lily of the Valley |  | all contributors died by 1908 |
| 1374 | Balzac, Honoré de | Vendetta |  | all contributors died by 1908 |
| 287 | Barr, Amelia E. | Remember the Alamo |  | all contributors died by 1919 |
| 420 | Baum, L. Frank (Lyman Frank) | Dorothy and the Wizard in Oz |  | all contributors died by 1919 |
| 961 | Baum, L. Frank (Lyman Frank) | Glinda of Oz In Which Are Related the Exciting Experiences of Princess Ozma of Oz, and Dor |  | all contributors died by 1919 |
| 486 | Baum, L. Frank (Lyman Frank) | Ozma of Oz A Record of Her Adventures with Dorothy Gale of Kansas, the Yellow Hen, the Sca |  | all contributors died by 1919 |
| 958 | Baum, L. Frank (Lyman Frank) | Rinkitink in Oz Wherein Is Recorded the Perilous Quest of Prince Inga of Pingaree and King |  | all contributors died by 1919 |
| 518 | Baum, L. Frank (Lyman Frank) | The Enchanted Island of Yew Whereon Prince Marvel Encountered the High Ki of Twi and Other |  | all contributors died by 1919 |
| 520 | Baum, L. Frank (Lyman Frank) | The Life and Adventures of Santa Claus |  | all contributors died by 1919 |
| 959 | Baum, L. Frank (Lyman Frank) | The Lost Princess of Oz |  | all contributors died by 1919 |
| 419 | Baum, L. Frank (Lyman Frank) | The Magic of Oz |  | all contributors died by 1919 |
| 485 | Baum, L. Frank (Lyman Frank) | The Road to Oz |  | all contributors died by 1919 |
| 960 | Baum, L. Frank (Lyman Frank) | The Tin Woodman of Oz A Faithful Story of the Astonishing Adventure Undertaken by the Tin  |  | all contributors died by 1919 |
| 55 | Baum, L. Frank (Lyman Frank) | The Wonderful Wizard of Oz |  | all contributors died by 1919 |
| 2060 | Beckford, William | The History of Caliph Vathek |  | all contributors died by 1894 |
| 375 | Bierce, Ambrose | An Occurrence at Owl Creek Bridge |  | all contributors died by 1914 |
| 840 | Blackmore, R. D. (Richard Doddridge) | Lorna Doone: A Romance of Exmoor |  | all contributors died by 1900 |
| 1198 | Boldrewood, Rolf | Robbery under Arms A Story of Life and Adventure in the Bush and in the Australian Goldfie |  | all contributors died by 1915 |
| 452 | Borrow, George | Lavengro: The Scholar, the Gypsy, the Priest | 1900 | front matter dated 1900 |
| 422 | Borrow, George | The Romany Rye |  | all contributors died by 1881 |
| 768 | Brontë, Emily | Wuthering Heights |  | all contributors died by 1848 |
| 792 | Brown, Charles Brockden | Wieland; Or, The Transformation: An American Tale |  | all contributors died by 1810 |
| 1356 | Bullen, Frank Thomas | The Cruise of the "Cachalot" Round the World After Sperm Whales |  | all contributors died by 1915 |
| 384 | Burnett, Frances Hodgson | The Lost Prince |  | all contributors died by 1924 |
| 459 | Burnett, Frances Hodgson | The White People |  | all contributors died by 1924 |
| 2058 | Byrne, Donn | Messer Marco Polo |  | all contributors died by 1928 |
| 1625 | Collins, Wilkie | The frozen deep |  | all contributors died by 1889 |
| 1476 | Conrad, Joseph | Chance: A Tale in Two Parts |  | all contributors died by 1924 |
| 2021 | Conrad, Joseph | Nostromo: A Tale of the Seaboard |  | all contributors died by 1924 |
| 1083 | Conrad, Joseph | The Arrow of Gold: A Story Between Two Notes |  | all contributors died by 1924 |
| 1712 | Conrad, Joseph | The Rescue: A Romance of the Shallows |  | all contributors died by 1924 |
| 220 | Conrad, Joseph | The Secret Sharer |  | all contributors died by 1924 |
| 451 | Conrad, Joseph | The Shadow Line: A Confession |  | all contributors died by 1924 |
| 1142 | Conrad, Joseph | Typhoon |  | all contributors died by 1924 |
| 525 | Conrad, Joseph | Youth, a Narrative |  | all contributors died by 1924 |
| 940 | Cooper, James Fenimore | The Last of the Mohicans; A narrative of 1757 |  | all contributors died by 1851 |
| 1880 | Cooper, James Fenimore | The Pathfinder; Or, The Inland Sea |  | all contributors died by 1851 |
| 1927 | Cooper, Susan Fenimore | Elinor Wyllys; Or, The Young Folk of Longbridge: A Tale. Volume 1 |  | all contributors died by 1894 |
| 1928 | Cooper, Susan Fenimore | Elinor Wyllys; Or, The Young Folk of Longbridge: A Tale. Volume 2 |  | all contributors died by 1894 |
| 73 | Crane, Stephen | The Red Badge of Courage: An Episode of the American Civil War |  | all contributors died by 1900 |
| 1817 | Davis, Richard Harding | A Question of Latitude |  | all contributors died by 1916 |
| 1761 | Davis, Richard Harding | My Buried Treasure |  | all contributors died by 1916 |
| 1824 | Davis, Richard Harding | Peace Manoeuvres |  | all contributors died by 1916 |
| 403 | Davis, Richard Harding | Soldiers of Fortune |  | all contributors died by 1916 |
| 411 | Davis, Richard Harding | The King's Jackal |  | all contributors died by 1916 |
| 1823 | Davis, Richard Harding | The Make-Believe Man |  | all contributors died by 1916 |
| 358 | Davis, Richard Harding | The Scarlet Car |  | all contributors died by 1916 |
| 2040 | De Quincey, Thomas | Confessions of an English Opium-Eater |  | all contributors died by 1859 |
| 376 | Defoe, Daniel | A Journal of the Plague Year Being Observations or Memorials of the Most Remarkable Occurr |  | all contributors died by 1731 |
| 561 | Defoe, Daniel | The Further Adventures of Robinson Crusoe |  | all contributors died by 1731 |
| 521 | Defoe, Daniel | The Life and Adventures of Robinson Crusoe |  | all contributors died by 1731 |
| 46 | Dickens, Charles | A Christmas Carol in Prose; Being a Ghost Story of Christmas |  | all contributors died by 1870 |
| 1407 | Dickens, Charles | A Message from the Sea |  | all contributors died by 1870 |
| 98 | Dickens, Charles | A Tale of Two Cities |  | all contributors died by 1870 |
| 968 | Dickens, Charles | Martin Chuzzlewit |  | all contributors died by 1870 |
| 588 | Dickens, Charles | Master Humphrey's Clock |  | all contributors died by 1870 |
| 1406 | Dickens, Charles | The Perils of Certain English Prisoners |  | all contributors died by 1870 |
| 1465 | Dickens, Charles | The Wreck of the Golden Mary |  | all contributors died by 1870 |
| 1289 | Dickens, Charles | Three Ghost Stories |  | all contributors died by 1870 |
| 1644 | Doyle, Arthur Conan | The Adventures of Gerard |  | all contributors died by 1930 |
| 294 | Doyle, Arthur Conan | The Captain of the Polestar, and Other Tales |  | all contributors died by 1930 |
| 139 | Doyle, Arthur Conan | The Lost World |  | all contributors died by 1930 |
| 903 | Doyle, Arthur Conan | The White Company |  | all contributors died by 1930 |
| 1258 | Dumas, Alexandre | Ten Years Later |  | all contributors died by 1870 |
| 1257 | Dumas, Alexandre; Maquet, Auguste | The three musketeers |  | all contributors died by 1888 |
| 1259 | Dumas, Alexandre; Maquet, Auguste | Twenty years after |  | all contributors died by 1888 |
| 1290 | Flaubert, Gustave | Salammbo |  | all contributors died by 1880 |
| 324 | Fox, John, Jr. | A Knight of the Cumberland |  | all contributors died by 1919 |
| 2059 | Fox, John, Jr. | The Little Shepherd of Kingdom Come |  | all contributors died by 1919 |
| 1235 | Gautier, Théophile | Captain Fracasse |  | all contributors died by 1872 |
| 711 | Haggard, H. Rider (Henry Rider) | Allan Quatermain |  | all contributors died by 1925 |
| 1711 | Haggard, H. Rider (Henry Rider) | Child of Storm |  | all contributors died by 1925 |
| 1724 | Haggard, H. Rider (Henry Rider) | Finished |  | all contributors died by 1925 |
| 2166 | Haggard, H. Rider (Henry Rider) | King Solomon's Mines |  | all contributors died by 1925 |
| 1918 | Haggard, H. Rider (Henry Rider) | Long Odds |  | all contributors died by 1925 |
| 1690 | Haggard, H. Rider (Henry Rider) | Marie: An Episode in the Life of the Late Allan Quatermain |  | all contributors died by 1925 |
| 1848 | Haggard, H. Rider (Henry Rider) | Montezuma's Daughter |  | all contributors died by 1925 |
| 1207 | Haggard, H. Rider (Henry Rider) | Nada the Lily |  | all contributors died by 1925 |
| 1368 | Haggard, H. Rider (Henry Rider) | When the World Shook Being an Account of the Great Adventure of Bastin, Bickley and Arbuth |  | all contributors died by 1925 |
| 1312 | Harte, Bret | Selected Stories of Bret Harte |  | all contributors died by 1902 |
| 512 | Hawthorne, Nathaniel | Mosses from an old manse |  | all contributors died by 1864 |
| 1916 | Hawthorne, Nathaniel | The Great Stone Face, and Other Tales of the White Mountains |  | all contributors died by 1864 |
| 77 | Hawthorne, Nathaniel | The House of the Seven Gables |  | all contributors died by 1864 |
| 33 | Hawthorne, Nathaniel | The Scarlet Letter |  | all contributors died by 1864 |
| 513 | Hawthorne, Nathaniel | The snow-image, and other twice-told tales |  | all contributors died by 1864 |
| 508 | Hawthorne, Nathaniel | Twice-Told Tales |  | all contributors died by 1864 |
| 717 | Hearn, Lafcadio | Chita: A Memory of Last Island |  | all contributors died by 1904 |
| 942 | Hudson, W. H. (William Henry) | Green Mansions: A Romance of the Tropical Forest |  | all contributors died by 1922 |
| 135 | Hugo, Victor | Les Misérables |  | all contributors died by 1928 |
| 1371 | Irving, Washington | Astoria; Or, Anecdotes of an Enterprise Beyond the Rocky Mountains |  | all contributors died by 1859 |
| 1190 | James, Henry | The Jolly Corner |  | all contributors died by 1916 |
| 1993 | Jerome, Jerome K. (Jerome Klapka) | Told After Supper |  | all contributors died by 1927 |
| 467 | La Fayette, Madame de (Marie-Madeleine Pioche de L | The Princess of Cleves |  | all contributors died by 1693 |
| 128 | Lang, Andrew | The Arabian Nights Entertainments |  | all contributors died by 1912 |
| 503 | Lang, Andrew | The Blue Fairy Book |  | all contributors died by 1912 |
| 1036 | Lawson, Henry | Joe Wilson and His Mates |  | all contributors died by 1922 |
| 601 | Lewis, M. G. (Matthew Gregory) | The Monk: A Romance |  | all contributors died by 1818 |
| 501 | Lofting, Hugh | The Story of Doctor Dolittle | 1920 | front matter dated 1920 |
| 1154 | Lofting, Hugh | The Voyages of Doctor Dolittle | 1922 | front matter dated 1922 |
| 1163 | London, Jack | Adventure |  | all contributors died by 1916 |
| 310 | London, Jack | Before Adam |  | all contributors died by 1916 |
| 1161 | London, Jack | Jerry of the Islands |  | all contributors died by 1916 |
| 710 | London, Jack | Love of Life, and Other Stories | 1907 | front matter dated 1907 |
| 1730 | London, Jack | Michael, Brother of Jerry |  | all contributors died by 1916 |
| 1596 | London, Jack | Smoke Bellew |  | all contributors died by 1916 |
| 1208 | London, Jack | South Sea Tales |  | all contributors died by 1916 |
| 911 | London, Jack | Tales of the Fish Patrol |  | all contributors died by 1916 |
| 1096 | London, Jack | The Faith of Men |  | all contributors died by 1916 |
| 788 | London, Jack | The Red One |  | all contributors died by 1916 |
| 1074 | London, Jack | The Sea-Wolf |  | all contributors died by 1916 |
| 215 | London, Jack | The call of the wild |  | all contributors died by 1916 |
| 910 | London, Jack | White Fang |  | all contributors died by 1916 |
| 1951 | Lytton, Edward Bulwer Lytton, Baron | The Coming Race |  | all contributors died by 1873 |
| 1565 | Lytton, Edward Bulwer Lytton, Baron | The Last Days of Pompeii |  | all contributors died by 1873 |
| 708 | MacDonald, George | The Princess and the Goblin |  | all contributors died by 1905 |
| 1412 | Marryat, Frederick | Masterman Ready |  | all contributors died by 1848 |
| 15 | Melville, Herman | Moby-Dick; or, The Whale |  | all contributors died by 1891 |
| 1900 | Melville, Herman | Typee: A Romance of the South Seas |  | all contributors died by 1908 |
| 357 | Morris, William | A Dream of John Ball; and, A King's Lesson |  | all contributors died by 1896 |
| 169 | Morris, William | The Well at the World's End: A Tale |  | all contributors died by 1896 |
| 1874 | Nesbit, E. (Edith) | The Railway Children |  | all contributors died by 1924 |
| 837 | Nesbit, E. (Edith) | The Story of the Amulet |  | all contributors died by 1924 |
| 770 | Nesbit, E. (Edith) | The Story of the Treasure Seekers Being the Adventures of the Bastable Children in Search  |  | all contributors died by 1924 |
| 794 | Nesbit, E. (Edith) | The Wouldbegoods: Being the Further Adventures of the Treasure Seekers |  | all contributors died by 1924 |
| 213 | Paterson, A. B. (Andrew Barton) | The Man from Snowy River | 1902 | front matter dated 1902 |
| 966 | Peacock, Thomas Love | Maid Marian |  | all contributors died by 1866 |
| 932 | Poe, Edgar Allan | The Fall of the House of Usher |  | all contributors died by 1849 |
| 468 | Prévost, abbé | Manon Lescaut |  | all contributors died by 1763 |
| 973 | Pyle, Howard | Howard Pyle's Book of Pirates Fiction, Fact & Fancy Concerning the Buccaneers & Marooners  |  | all contributors died by 1911 |
| 1557 | Pyle, Howard | Men of Iron |  | all contributors died by 1911 |
| 964 | Pyle, Howard | The Merry Adventures of Robin Hood |  | all contributors died by 1911 |
| 1366 | Reade, Charles | The Cloister and the Hearth |  | all contributors died by 1884 |
| 1194 | Rougemont, Louis de | The Adventures of Louis de Rougemont |  | all contributors died by 1921 |
| 1441 | Schreiner, Olive | The Story of an African Farm |  | all contributors died by 1920 |
| 1461 | Scott, Walter | A Legend of Montrose |  | all contributors died by 1832 |
| 82 | Scott, Walter | Ivanhoe: A Romance |  | all contributors died by 1832 |
| 1606 | Scott, Walter | Kenilworth |  | all contributors died by 1832 |
| 1460 | Scott, Walter | The Black Dwarf |  | all contributors died by 1832 |
| 471 | Scott, Walter | The Bride of Lammermoor |  | all contributors died by 1832 |
| 1377 | Scott, Walter | The Talisman |  | all contributors died by 1832 |
| 1668 | Scott, Walter | The Tapestried Chamber, and Death of the Laird's Jock |  | all contributors died by 1832 |
| 2034 | Scott, Walter | Waverley; or, 'Tis sixty years since |  | all contributors died by 1832 |
| 259 | Service, Robert W. (Robert William) | Ballads of a Cheechako | 1909 | front matter dated 1909 |
| 271 | Sewell, Anna | Black Beauty |  | all contributors died by 1878 |
| 84 | Shelley, Mary Wollstonecraft | Frankenstein; or, The modern Prometheus |  | all contributors died by 1851 |
| 589 | Stevenson, Robert Louis | Catriona |  | all contributors died by 1894 |
| 421 | Stevenson, Robert Louis | Kidnapped |  | all contributors died by 1894 |
| 839 | Stevenson, Robert Louis | New Arabian Nights |  | all contributors died by 1894 |
| 372 | Stevenson, Robert Louis | Prince Otto, a Romance |  | all contributors died by 1894 |
| 322 | Stevenson, Robert Louis | St. Ives: Being the Adventures of a French Prisoner in England |  | all contributors died by 1894 |
| 848 | Stevenson, Robert Louis | The Black Arrow: A Tale of the Two Roses |  | all contributors died by 1894 |
| 864 | Stevenson, Robert Louis | The Master of Ballantrae: A Winter's Tale |  | all contributors died by 1894 |
| 120 | Stevenson, Robert Louis | Treasure Island |  | all contributors died by 1926 |
| 1188 | Stoker, Bram | The Lair of the White Worm |  | all contributors died by 1912 |
| 286 | Stratton-Porter, Gene | Laddie: A True Blue Story |  | all contributors died by 1924 |
| 829 | Swift, Jonathan | Gulliver's Travels into Several Remote Nations of the World |  | all contributors died by 1745 |
| 1086 | Twain, Mark | A Horse's Tale |  | all contributors died by 1910 |
| 74 | Twain, Mark | The Adventures of Tom Sawyer, Complete |  | all contributors died by 1910 |
| 1837 | Twain, Mark | The Prince and the Pauper |  | all contributors died by 1910 |
| 91 | Twain, Mark | Tom Sawyer Abroad |  | all contributors died by 1910 |
| 103 | Verne, Jules | Around the World in Eighty Days |  | all contributors died by 1905 |
| 2083 | Verne, Jules | In Search of the Castaways; Or, The Children of Captain Grant |  | all contributors died by 1905 |
| 1842 | Verne, Jules | Michael Strogoff; Or, The Courier of the Czar |  | all contributors died by 1905 |
| 1353 | Verne, Jules | Off on a Comet! a Journey through Planetary Space |  | all contributors died by 1905 |
| 1268 | Verne, Jules | The Mysterious Island |  | all contributors died by 1913 |
| 1698 | Verne, Jules | The Survivors of the Chancellor |  | all contributors died by 1905 |
| 1355 | Verne, Jules | The Underground City; Or, The Black Indies (Sometimes Called The Child of the Cavern) |  | all contributors died by 1905 |
| 164 | Verne, Jules | Twenty Thousand Leagues under the Sea |  | all contributors died by 1905 |
| 696 | Walpole, Horace | The Castle of Otranto |  | all contributors died by 1894 |
| 1939 | Weyman, Stanley John | A Gentleman of France: Being the Memoirs of Gaston de Bonne Sieur de Marsac |  | all contributors died by 1928 |
| 2041 | Weyman, Stanley John | The House of the Wolf: A Romance |  | all contributors died by 1928 |
| 1896 | Weyman, Stanley John | Under the red robe |  | all contributors died by 1928 |
| 1033 | Wiggin, Kate Douglas Smith | Rose o' the River |  | all contributors died by 1923 |
| 174 | Wilde, Oscar | The Picture of Dorian Gray |  | all contributors died by 1900 |

## crime (76 books)

| Gutenberg ID | Author | Title | Year | PD basis |
|---|---|---|---|---|
| 2031 | Abbott, David P. (David Phelps); Carrington, Herew | The Lock and Key Library: The Most Interesting Stories of All Nations: Real Life | 1908 | front matter dated 1908 |
| 528 | Alger, Horatio, Jr. | Joe the Hotel Boy; Or, Winning out by Pluck |  | all contributors died by 1899 |
| 1678 | Balzac, Honoré de | An Historical Mystery (The Gondreville Mystery) |  | all contributors died by 1908 |
| 1433 | Balzac, Honoré de | The Red Inn |  | all contributors died by 1908 |
| 436 | Baum, L. Frank (Lyman Frank) | The Master Key An Electrical Fairy Tale Founded Upon the Mysteries of Electricity |  | all contributors died by 1919 |
| 331 | Burroughs, Edgar Rice | The Mucker | 1916 | front matter dated 1916 |
| 1696 | Chesterton, G. K. (Gilbert Keith) | The Club of Queer Trades | 1905 | known first publication: first published 1905 |
| 1720 | Chesterton, G. K. (Gilbert Keith) | The Man Who Knew Too Much | 1922 | known first publication: first published 1922 |
| 1695 | Chesterton, G. K. (Gilbert Keith) | The Man Who Was Thursday: A Nightmare | 1908 | known first publication: first published 1908 |
| 204 | Chesterton, G. K. (Gilbert Keith) | The innocence of Father Brown | 1911 | known first publication: first published 1911 |
| 223 | Chesterton, G. K. (Gilbert Keith) | The wisdom of Father Brown | 1914 | known first publication: first published 1914 |
| 863 | Christie, Agatha | The Mysterious Affair at Styles | 1920 | known first publication: first published 1920 |
| 1155 | Christie, Agatha | The Secret Adversary | 1922 | known first publication: first published 1922 |
| 1629 | Collins, Wilkie | "I Say No" |  | all contributors died by 1889 |
| 1626 | Collins, Wilkie | After Dark |  | all contributors died by 1889 |
| 1895 | Collins, Wilkie | Armadale |  | all contributors died by 1889 |
| 1621 | Collins, Wilkie | Miss or Mrs.? |  | all contributors died by 1889 |
| 1628 | Collins, Wilkie | My Lady's Money |  | all contributors died by 1889 |
| 1587 | Collins, Wilkie | The Black Robe |  | all contributors died by 1889 |
| 1627 | Collins, Wilkie | The Evil Genius: A Domestic Story |  | all contributors died by 1889 |
| 170 | Collins, Wilkie | The Haunted Hotel: A Mystery of Modern Venice |  | all contributors died by 1889 |
| 1622 | Collins, Wilkie | The Law and the Lady |  | all contributors died by 1889 |
| 1975 | Collins, Wilkie | The Legacy of Cain |  | all contributors died by 1889 |
| 155 | Collins, Wilkie | The Moonstone |  | all contributors died by 1889 |
| 1917 | Collins, Wilkie | The Queen of Hearts |  | all contributors died by 1889 |
| 583 | Collins, Wilkie | The Woman in White |  | all contributors died by 1889 |
| 974 | Conrad, Joseph | The Secret Agent: A Simple Tale |  | all contributors died by 1924 |
| 1822 | Davis, Richard Harding | The Amateur |  | all contributors died by 1916 |
| 1806 | Davis, Richard Harding | The Frame Up |  | all contributors died by 1916 |
| 1807 | Davis, Richard Harding | The Lost House |  | all contributors died by 1916 |
| 1818 | Davis, Richard Harding | The Spy |  | all contributors died by 1916 |
| 370 | Defoe, Daniel | The Fortunes and Misfortunes of the Famous Moll Flanders |  | all contributors died by 1731 |
| 917 | Dickens, Charles | Barnaby Rudge: A Tale of the Riots of 'Eighty |  | all contributors died by 1870 |
| 807 | Dickens, Charles | Hunted Down: The Detective Stories of Charles Dickens |  | all contributors died by 1870 |
| 730 | Dickens, Charles | Oliver Twist |  | all contributors died by 1870 |
| 564 | Dickens, Charles | The Mystery of Edwin Drood |  | all contributors died by 1870 |
| 924 | Dickens, Charles | To Be Read at Dusk |  | all contributors died by 1870 |
| 1423 | Dickens, Charles; Collins, Wilkie | No Thoroughfare |  | all contributors died by 1889 |
| 244 | Doyle, Arthur Conan | A Study in Scarlet |  | all contributors died by 1930 |
| 537 | Doyle, Arthur Conan | Tales of Terror and Mystery |  | all contributors died by 1930 |
| 1661 | Doyle, Arthur Conan | The Adventures of Sherlock Holmes |  | all contributors died by 1930 |
| 834 | Doyle, Arthur Conan | The Memoirs of Sherlock Holmes |  | all contributors died by 1930 |
| 355 | Doyle, Arthur Conan | The Parasite: A Story |  | all contributors died by 1930 |
| 108 | Doyle, Arthur Conan | The Return of Sherlock Holmes |  | all contributors died by 1930 |
| 2097 | Doyle, Arthur Conan | The Sign of the Four |  | all contributors died by 1930 |
| 2123 | France, Anatole | The Crime of Sylvestre Bonnard |  | all contributors died by 1924 |
| 298 | Frederic, Harold | The Market-Place |  | all contributors died by 1898 |
| 1617 | Freeman, Mary Eleanor Wilkins | The Wind in the Rose-Bush, and Other Stories of the Supernatural |  | all contributors died by 1930 |
| 547 | Gaboriau, Emile | Baron Trigault's Vengeance |  | all contributors died by 1873 |
| 1748 | Gaboriau, Emile | Other People's Money |  | all contributors died by 1873 |
| 305 | Gaboriau, Emile | The Count's Millions |  | all contributors died by 1873 |
| 1651 | Gaboriau, Emile | The Mystery of Orcival |  | all contributors died by 1873 |
| 2153 | Gaskell, Elizabeth Cleghorn | Mary Barton |  | all contributors died by 1865 |
| 1081 | Gogol, Nikolai Vasilevich | Dead Souls | 1842 | front matter dated 1842 |
| 2098 | Hornung, E. W. (Ernest William) | A Thief in the Night: A Book of Raffles' Adventures |  | all contributors died by 1921 |
| 707 | Hornung, E. W. (Ernest William) | Raffles: Further Adventures of the Amateur Cracksman |  | all contributors died by 1921 |
| 706 | Hornung, E. W. (Ernest William) | The Amateur Cracksman |  | all contributors died by 1921 |
| 446 | Irving, H. B. (Henry Brodribb) | A Book of Remarkable Criminals |  | all contributors died by 1919 |
| 209 | James, Henry | The Turn of the Screw |  | all contributors died by 1916 |
| 509 | Le Fanu, Joseph Sheridan | The Purcell Papers — Volume 1 |  | all contributors died by 1873 |
| 510 | Le Fanu, Joseph Sheridan | The Purcell Papers — Volume 2 |  | all contributors died by 1873 |
| 175 | Leroux, Gaston | The Phantom of the Opera |  | all contributors died by 1927 |
| 1686 | Leroux, Gaston | The Secret of the Night |  | all contributors died by 1927 |
| 636 | Mackay, Charles | Memoirs of Extraordinary Popular Delusions — Volume 1 |  | all contributors died by 1889 |
| 713 | Mackay, Charles | Memoirs of Extraordinary Popular Delusions — Volume 2 |  | all contributors died by 1889 |
| 884 | Mackay, Charles | Memoirs of Extraordinary Popular Delusions — Volume 3 |  | all contributors died by 1889 |
| 431 | Phillips, David Graham | The Fortune Hunter |  | all contributors died by 1911 |
| 1923 | Reeve, Arthur B. (Arthur Benjamin) | The Poisoned Pen | 1911 | front matter dated 1911 |
| 434 | Rinehart, Mary Roberts | The Circular Staircase | 1908 | known first publication: first published 1908 |
| 1869 | Rinehart, Mary Roberts | The Man in Lower Ten | 1909 | known first publication: first published 1909 |
| 42 | Stevenson, Robert Louis | The strange case of Dr. Jekyll and Mr. Hyde |  | all contributors died by 1894 |
| 647 | Stevenson, Robert Louis; Stevenson, Fanny Van de G | The Dynamiter |  | all contributors died by 1914 |
| 1478 | Stewart, Donald Ogden | A Parody Outline of History Wherein May Be Found a Curiously Irreverent Treatment of Ameri | 1916 | front matter dated 1916 |
| 345 | Stoker, Bram | Dracula |  | all contributors died by 1912 |
| 102 | Twain, Mark | The Tragedy of Pudd'nhead Wilson |  | all contributors died by 1910 |
| 93 | Twain, Mark | Tom Sawyer, Detective |  | all contributors died by 1910 |

## noir (2 books)

| Gutenberg ID | Author | Title | Year | PD basis |
|---|---|---|---|---|
| 1218 | Packard, Frank L. (Frank Lucius) | The Adventures of Jimmie Dale | 1917 | known first publication: first published 1917 |
| 1741 | Packard, Frank L. (Frank Lucius) | The White Moll | 1920 | known first publication: first published 1920 |
