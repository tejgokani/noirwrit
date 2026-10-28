# Data sources

All texts come from Project Gutenberg (gutenberg.org), which hosts works it has cleared as public domain in the United States.
Noirwrit applies a stricter rule on top: the work must be published in 1930 or earlier. A title is kept only when one of these holds:

1. Every listed contributor (author, translator, editor) died in 1930 or earlier.
2. The first publication year is well established and is 1930 or earlier (listed in `noirwrit/corpus/catalog.py`, `KNOWN_YEARS`).
3. A pulp issue date in the title is 1930 or earlier.
4. The book's own front matter carries a copyright or publication year, and the latest one is 1930 or earlier.

Any book whose front matter mentions a year after 1930 is left out, even when another rule passes. Unsure means out.

Kept: 1828 books. Dropped: 1311 (reasons in `data/dropped.jsonl`).

## general (341 books)

| Gutenberg ID | Author | Title | Year | PD basis |
|---|---|---|---|---|
| 2866 | Ainsworth, William Harrison | Windsor Castle |  | all contributors died by 1882 |
| 3795 | Alcott, Louisa May | Under the Lilacs |  | all contributors died by 1888 |
| 1757 | Aldrich, Thomas Bailey | The Cruise of the Dolphin |  | all contributors died by 1907 |
| 293 | Alger, Horatio, Jr. | Paul Prescott's Charge |  | all contributors died by 1899 |
| 296 | Alger, Horatio, Jr. | The Cash Boy |  | all contributors died by 1899 |
| 1078 | Altsheler, Joseph A. (Joseph Alexander) | The Scouts of the Valley |  | all contributors died by 1919 |
| 615 | Ariosto, Lodovico | Orlando Furioso |  | all contributors died by 1843 |
| 1607 | Astor, John Jacob | A Journey in Other Worlds: A Romance of the Future |  | all contributors died by 1912 |
| 121 | Austen, Jane | Northanger Abbey |  | all contributors died by 1817 |
| 783 | Badger, Jos. E. (Joseph Edward) | The Lost City |  | all contributors died by 1909 |
| 646 | Ballantyne, R. M. (Robert Michael) | The Coral Island: A Tale of the Pacific Ocean |  | all contributors died by 1894 |
| 4795 | Ballou, Maturin M. (Maturin Murray) | The Circassian Slave, or, the Sultan's favorite : a story of Constantinople and the Caucas |  | all contributors died by 1895 |
| 4675 | Ballou, Maturin M. (Maturin Murray) | The Sea-Witch; Or, The African Quadroon: A Story of the Slave Coast |  | all contributors died by 1895 |
| 1456 | Balzac, Honoré de | An Episode under the Terror |  | all contributors died by 1927 |
| 1454 | Balzac, Honoré de | Maitre Cornelius |  | all contributors died by 1908 |
| 1569 | Balzac, Honoré de | The Lily of the Valley |  | all contributors died by 1908 |
| 1374 | Balzac, Honoré de | Vendetta |  | all contributors died by 1908 |
| 287 | Barr, Amelia E. | Remember the Alamo |  | all contributors died by 1919 |
| 4982 | Barr, Robert | A Rock in the Baltic |  | all contributors died by 1912 |
| 420 | Baum, L. Frank (Lyman Frank) | Dorothy and the Wizard in Oz |  | all contributors died by 1919 |
| 961 | Baum, L. Frank (Lyman Frank) | Glinda of Oz In Which Are Related the Exciting Experiences of Princess Ozma of Oz, and Dor |  | all contributors died by 1919 |
| 486 | Baum, L. Frank (Lyman Frank) | Ozma of Oz A Record of Her Adventures with Dorothy Gale of Kansas, the Yellow Hen, the Sca |  | all contributors died by 1919 |
| 958 | Baum, L. Frank (Lyman Frank) | Rinkitink in Oz Wherein Is Recorded the Perilous Quest of Prince Inga of Pingaree and King |  | all contributors died by 1919 |
| 518 | Baum, L. Frank (Lyman Frank) | The Enchanted Island of Yew Whereon Prince Marvel Encountered the High Ki of Twi and Other |  | all contributors died by 1919 |
| 520 | Baum, L. Frank (Lyman Frank) | The Life and Adventures of Santa Claus |  | all contributors died by 1919 |
| 959 | Baum, L. Frank (Lyman Frank) | The Lost Princess of Oz |  | all contributors died by 1919 |
| 419 | Baum, L. Frank (Lyman Frank) | The Magic of Oz |  | all contributors died by 1919 |
| 485 | Baum, L. Frank (Lyman Frank) | The Road to Oz |  | all contributors died by 1919 |
| 4358 | Baum, L. Frank (Lyman Frank) | The Sea Fairies |  | all contributors died by 1919 |
| 960 | Baum, L. Frank (Lyman Frank) | The Tin Woodman of Oz A Faithful Story of the Astonishing Adventure Undertaken by the Tin  |  | all contributors died by 1919 |
| 55 | Baum, L. Frank (Lyman Frank) | The Wonderful Wizard of Oz |  | all contributors died by 1919 |
| 3818 | Becke, Louis | By Reef and Palm |  | all contributors died by 1913 |
| 2060 | Beckford, William | The History of Caliph Vathek |  | all contributors died by 1894 |
| 375 | Bierce, Ambrose | An Occurrence at Owl Creek Bridge |  | all contributors died by 1914 |
| 840 | Blackmore, R. D. (Richard Doddridge) | Lorna Doone: A Romance of Exmoor |  | all contributors died by 1900 |
| 1198 | Boldrewood, Rolf | Robbery under Arms A Story of Life and Adventure in the Bush and in the Australian Goldfie |  | all contributors died by 1915 |
| 452 | Borrow, George | Lavengro: The Scholar, the Gypsy, the Priest | 1900 | front matter dated 1900 |
| 422 | Borrow, George | The Romany Rye |  | all contributors died by 1881 |
| 768 | Brontë, Emily | Wuthering Heights |  | all contributors died by 1848 |
| 792 | Brown, Charles Brockden | Wieland; Or, The Transformation: An American Tale |  | all contributors died by 1810 |
| 3782 | Buchan, John | Huntingtower | 1922 | front matter dated 1922 |
| 1356 | Bullen, Frank Thomas | The Cruise of the "Cachalot" Round the World After Sperm Whales |  | all contributors died by 1915 |
| 384 | Burnett, Frances Hodgson | The Lost Prince |  | all contributors died by 1924 |
| 459 | Burnett, Frances Hodgson | The White People |  | all contributors died by 1924 |
| 2058 | Byrne, Donn | Messer Marco Polo |  | all contributors died by 1928 |
| 4353 | Chester, George Randolph | Five Thousand an Hour: How Johnny Gamble Won the Heiress |  | all contributors died by 1924 |
| 3424 | Clarke, Marcus Andrew Hislop | For the Term of His Natural Life |  | all contributors died by 1881 |
| 3606 | Collins, Wilkie | Antonina; Or, The Fall of Rome |  | all contributors died by 1889 |
| 1625 | Collins, Wilkie | The frozen deep |  | all contributors died by 1889 |
| 1476 | Conrad, Joseph | Chance: A Tale in Two Parts |  | all contributors died by 1924 |
| 2021 | Conrad, Joseph | Nostromo: A Tale of the Seaboard |  | all contributors died by 1924 |
| 1083 | Conrad, Joseph | The Arrow of Gold: A Story Between Two Notes |  | all contributors died by 1924 |
| 1712 | Conrad, Joseph | The Rescue: A Romance of the Shallows |  | all contributors died by 1924 |
| 220 | Conrad, Joseph | The Secret Sharer |  | all contributors died by 1924 |
| 451 | Conrad, Joseph | The Shadow Line: A Confession |  | all contributors died by 1924 |
| 1142 | Conrad, Joseph | Typhoon |  | all contributors died by 1924 |
| 525 | Conrad, Joseph | Youth, a Narrative |  | all contributors died by 1924 |
| 4796 | Cooper, James Fenimore | Jack Tier; Or, The Florida Reef |  | all contributors died by 1851 |
| 4215 | Cooper, James Fenimore | Oak Openings |  | all contributors died by 1851 |
| 3285 | Cooper, James Fenimore | The Deerslayer |  | all contributors died by 1851 |
| 940 | Cooper, James Fenimore | The Last of the Mohicans; A narrative of 1757 |  | all contributors died by 1851 |
| 1880 | Cooper, James Fenimore | The Pathfinder; Or, The Inland Sea |  | all contributors died by 1851 |
| 2275 | Cooper, James Fenimore | The Pioneers; Or, The Sources of the Susquehanna |  | all contributors died by 1851 |
| 1927 | Cooper, Susan Fenimore | Elinor Wyllys; Or, The Young Folk of Longbridge: A Tale. Volume 1 |  | all contributors died by 1894 |
| 1928 | Cooper, Susan Fenimore | Elinor Wyllys; Or, The Young Folk of Longbridge: A Tale. Volume 2 |  | all contributors died by 1894 |
| 73 | Crane, Stephen | The Red Badge of Courage: An Episode of the American Civil War |  | all contributors died by 1900 |
| 4539 | Curwood, James Oliver | Back to God's Country and Other Stories |  | all contributors died by 1927 |
| 4748 | Curwood, James Oliver | Baree, son of Kazan |  | all contributors died by 1927 |
| 4703 | Curwood, James Oliver | Flower of the North: A Modern Romance |  | all contributors died by 1927 |
| 4585 | Curwood, James Oliver | God's Country—And the Woman |  | all contributors died by 1927 |
| 4704 | Curwood, James Oliver | Nomads of the North: A Story of Romance and Adventure under the Open Stars |  | all contributors died by 1927 |
| 4743 | Curwood, James Oliver | The Country Beyond: A Romance of the Wilderness |  | all contributors died by 1927 |
| 1817 | Davis, Richard Harding | A Question of Latitude |  | all contributors died by 1916 |
| 1761 | Davis, Richard Harding | My Buried Treasure |  | all contributors died by 1916 |
| 1824 | Davis, Richard Harding | Peace Manoeuvres |  | all contributors died by 1916 |
| 403 | Davis, Richard Harding | Soldiers of Fortune |  | all contributors died by 1916 |
| 411 | Davis, Richard Harding | The King's Jackal |  | all contributors died by 1916 |
| 1823 | Davis, Richard Harding | The Make-Believe Man |  | all contributors died by 1916 |
| 358 | Davis, Richard Harding | The Scarlet Car |  | all contributors died by 1916 |
| 4506 | De Mille, James | Lost in the Fog |  | all contributors died by 1880 |
| 2040 | De Quincey, Thomas | Confessions of an English Opium-Eater |  | all contributors died by 1859 |
| 376 | Defoe, Daniel | A Journal of the Plague Year Being Observations or Memorials of the Most Remarkable Occurr |  | all contributors died by 1731 |
| 561 | Defoe, Daniel | The Further Adventures of Robinson Crusoe |  | all contributors died by 1731 |
| 521 | Defoe, Daniel | The Life and Adventures of Robinson Crusoe |  | all contributors died by 1731 |
| 46 | Dickens, Charles | A Christmas Carol in Prose; Being a Ghost Story of Christmas |  | all contributors died by 1870 |
| 1407 | Dickens, Charles | A Message from the Sea |  | all contributors died by 1870 |
| 98 | Dickens, Charles | A Tale of Two Cities |  | all contributors died by 1870 |
| 968 | Dickens, Charles | Martin Chuzzlewit |  | all contributors died by 1870 |
| 588 | Dickens, Charles | Master Humphrey's Clock |  | all contributors died by 1870 |
| 644 | Dickens, Charles | The Haunted Man and the Ghost's Bargain |  | all contributors died by 1870 |
| 1406 | Dickens, Charles | The Perils of Certain English Prisoners |  | all contributors died by 1870 |
| 1465 | Dickens, Charles | The Wreck of the Golden Mary |  | all contributors died by 1870 |
| 1289 | Dickens, Charles | Three Ghost Stories |  | all contributors died by 1870 |
| 2845 | Doyle, Arthur Conan | Sir Nigel |  | all contributors died by 1930 |
| 1644 | Doyle, Arthur Conan | The Adventures of Gerard |  | all contributors died by 1930 |
| 294 | Doyle, Arthur Conan | The Captain of the Polestar, and Other Tales |  | all contributors died by 1930 |
| 139 | Doyle, Arthur Conan | The Lost World |  | all contributors died by 1930 |
| 903 | Doyle, Arthur Conan | The White Company |  | all contributors died by 1930 |
| 1258 | Dumas, Alexandre | Ten Years Later |  | all contributors died by 1870 |
| 2681 | Dumas, Alexandre | Ten Years Later |  | all contributors died by 1870 |
| 2759 | Dumas, Alexandre | The Man in the Iron Mask |  | all contributors died by 1870 |
| 2710 | Dumas, Alexandre; Maquet, Auguste | Louise de la Vallière |  | all contributors died by 1888 |
| 1184 | Dumas, Alexandre; Maquet, Auguste | The Count of Monte Cristo |  | all contributors died by 1888 |
| 1257 | Dumas, Alexandre; Maquet, Auguste | The three musketeers |  | all contributors died by 1888 |
| 1259 | Dumas, Alexandre; Maquet, Auguste | Twenty years after |  | all contributors died by 1888 |
| 3007 | Emerson, Willis George | The Smoky God; Or, A Voyage to the Inner World |  | all contributors died by 1918 |
| 1290 | Flaubert, Gustave | Salammbo |  | all contributors died by 1880 |
| 2950 | Fleming, May Agnes | The Midnight Queen |  | all contributors died by 1880 |
| 324 | Fox, John, Jr. | A Knight of the Cumberland |  | all contributors died by 1919 |
| 3025 | Fox, John, Jr. | A Mountain Europa |  | all contributors died by 1919 |
| 2059 | Fox, John, Jr. | The Little Shepherd of Kingdom Come |  | all contributors died by 1919 |
| 2809 | Garland, Hamlin | Main-Travelled Roads | 1893 | front matter dated 1893 |
| 4537 | Gaskell, Elizabeth Cleghorn | Sylvia's Lovers — Complete |  | all contributors died by 1865 |
| 2549 | Gaskell, Elizabeth Cleghorn | The Doom of the Griffiths |  | all contributors died by 1865 |
| 1235 | Gautier, Théophile | Captain Fracasse |  | all contributors died by 1872 |
| 4306 | Gissing, George | Veranilda |  | all contributors died by 1903 |
| 3457 | Grey, Zane | The Man of the Forest | 1919 | front matter dated 1919 |
| 2729 | Haggard, H. Rider (Henry Rider) | A Tale of Three Lions |  | all contributors died by 1925 |
| 2857 | Haggard, H. Rider (Henry Rider) | A Yellow God: An Idol of Africa |  | all contributors died by 1925 |
| 711 | Haggard, H. Rider (Henry Rider) | Allan Quatermain |  | all contributors died by 1925 |
| 2727 | Haggard, H. Rider (Henry Rider) | Allan's Wife |  | all contributors died by 1925 |
| 2761 | Haggard, H. Rider (Henry Rider) | Benita, an African romance |  | all contributors died by 1925 |
| 2842 | Haggard, H. Rider (Henry Rider) | Black Heart and White Heart: A Zulu Idyll |  | all contributors died by 1925 |
| 1711 | Haggard, H. Rider (Henry Rider) | Child of Storm |  | all contributors died by 1925 |
| 2769 | Haggard, H. Rider (Henry Rider) | Cleopatra |  | all contributors died by 1925 |
| 2855 | Haggard, H. Rider (Henry Rider) | Elissa; Or, The Doom of Zimbabwe |  | all contributors died by 1925 |
| 2721 | Haggard, H. Rider (Henry Rider) | Eric Brighteyes |  | all contributors died by 1925 |
| 1724 | Haggard, H. Rider (Henry Rider) | Finished |  | all contributors died by 1925 |
| 2728 | Haggard, H. Rider (Henry Rider) | Hunter Quatermain's Story |  | all contributors died by 1925 |
| 2166 | Haggard, H. Rider (Henry Rider) | King Solomon's Mines |  | all contributors died by 1925 |
| 1918 | Haggard, H. Rider (Henry Rider) | Long Odds |  | all contributors died by 1925 |
| 2713 | Haggard, H. Rider (Henry Rider) | Maiwa's Revenge; Or, The War of the Little Hand |  | all contributors died by 1925 |
| 1690 | Haggard, H. Rider (Henry Rider) | Marie: An Episode in the Life of the Late Allan Quatermain |  | all contributors died by 1925 |
| 1848 | Haggard, H. Rider (Henry Rider) | Montezuma's Daughter |  | all contributors died by 1925 |
| 1207 | Haggard, H. Rider (Henry Rider) | Nada the Lily |  | all contributors died by 1925 |
| 2602 | Haggard, H. Rider (Henry Rider) | Queen Sheba's Ring |  | all contributors died by 1925 |
| 3155 | Haggard, H. Rider (Henry Rider) | She |  | all contributors died by 1925 |
| 4074 | Haggard, H. Rider (Henry Rider) | Swallow: A Tale of the Great Trek |  | all contributors died by 1925 |
| 2762 | Haggard, H. Rider (Henry Rider) | The Brethren |  | all contributors died by 1925 |
| 2841 | Haggard, H. Rider (Henry Rider) | The Ivory Child |  | all contributors died by 1925 |
| 2764 | Haggard, H. Rider (Henry Rider) | The Mahatma and the Hare: A Dream Story |  | all contributors died by 1925 |
| 3153 | Haggard, H. Rider (Henry Rider) | The Virgin of the Sun |  | all contributors died by 1925 |
| 3097 | Haggard, H. Rider (Henry Rider) | The Wanderer's Necklace |  | all contributors died by 1925 |
| 2893 | Haggard, H. Rider (Henry Rider) | The Wizard |  | all contributors died by 1925 |
| 1368 | Haggard, H. Rider (Henry Rider) | When the World Shook Being an Account of the Great Adventure of Bastin, Bickley and Arbuth |  | all contributors died by 1925 |
| 2763 | Haggard, H. Rider (Henry Rider); Lang, Andrew | The World's Desire |  | all contributors died by 1925 |
| 3046 | Harben, Will N. (Will Nathaniel) | The Land of the Changing Sun |  | all contributors died by 1919 |
| 2864 | Hardy, Thomas | The Trumpet-Major |  | all contributors died by 1928 |
| 2712 | Harte, Bret | A Drift from Redwood Camp |  | all contributors died by 1902 |
| 2723 | Harte, Bret | A First Family of Tasajara |  | all contributors died by 1902 |
| 2280 | Harte, Bret | A Millionaire of Rough-and-Ready |  | all contributors died by 1902 |
| 2692 | Harte, Bret | A Protegee of Jack Hamlin's, and Other Stories |  | all contributors died by 1902 |
| 2867 | Harte, Bret | A Sappho of Green Springs |  | all contributors died by 1902 |
| 2279 | Harte, Bret | A Waif of the Plains |  | all contributors died by 1902 |
| 2784 | Harte, Bret | Colonel Starbottle's Client |  | all contributors died by 1902 |
| 2286 | Harte, Bret | Devil's Ford |  | all contributors died by 1902 |
| 2793 | Harte, Bret | Flip: A California Romance |  | all contributors died by 1902 |
| 2794 | Harte, Bret | Found at Blazing Star |  | all contributors died by 1902 |
| 2180 | Harte, Bret | In a Hollow of the Hills |  | all contributors died by 1902 |
| 2695 | Harte, Bret | Jeff Briggs's Love Story |  | all contributors died by 1902 |
| 2185 | Harte, Bret | Maruja |  | all contributors died by 1902 |
| 2556 | Harte, Bret | Mr. Jack Hamlin's Mediation |  | all contributors died by 1902 |
| 2597 | Harte, Bret | Mrs. Skagg's Husbands and Other Stories |  | all contributors died by 1902 |
| 2574 | Harte, Bret | On the Frontier |  | all contributors died by 1902 |
| 2535 | Harte, Bret | Openings in the Old Trail |  | all contributors died by 1902 |
| 2705 | Harte, Bret | Sally Dows |  | all contributors died by 1902 |
| 1312 | Harte, Bret | Selected Stories of Bret Harte |  | all contributors died by 1902 |
| 2297 | Harte, Bret | Snow-Bound at Eagle's |  | all contributors died by 1902 |
| 2550 | Harte, Bret | Tales of Trail and Town |  | all contributors died by 1902 |
| 2886 | Harte, Bret | Tales of the Argonauts |  | all contributors died by 1902 |
| 2676 | Harte, Bret | The Bell-Ringer of Angel's, and Other Stories |  | all contributors died by 1902 |
| 2471 | Harte, Bret | The Crusade of the Excelsior |  | all contributors died by 1902 |
| 2281 | Harte, Bret | The Heritage of Dedlow Marsh and Other Tales |  | all contributors died by 1902 |
| 2798 | Harte, Bret | The Queen of the Pirate Isle |  | all contributors died by 1902 |
| 2560 | Harte, Bret | The Three Partners |  | all contributors died by 1902 |
| 2862 | Harte, Bret | The Twins of Table Mountain, and Other Stories |  | all contributors died by 1902 |
| 2459 | Harte, Bret | Trent's Trust, and Other Stories |  | all contributors died by 1902 |
| 512 | Hawthorne, Nathaniel | Mosses from an old manse |  | all contributors died by 1864 |
| 1916 | Hawthorne, Nathaniel | The Great Stone Face, and Other Tales of the White Mountains |  | all contributors died by 1864 |
| 77 | Hawthorne, Nathaniel | The House of the Seven Gables |  | all contributors died by 1864 |
| 33 | Hawthorne, Nathaniel | The Scarlet Letter |  | all contributors died by 1864 |
| 513 | Hawthorne, Nathaniel | The snow-image, and other twice-told tales |  | all contributors died by 1864 |
| 508 | Hawthorne, Nathaniel | Twice-Told Tales |  | all contributors died by 1864 |
| 717 | Hearn, Lafcadio | Chita: A Memory of Last Island |  | all contributors died by 1904 |
| 4932 | Henty, G. A. (George Alfred) | A Knight of the White Cross: A Tale of the Siege of Rhodes |  | all contributors died by 1902 |
| 4792 | Henty, G. A. (George Alfred) | In Freedom's Cause : A Story of Wallace and Bruce |  | all contributors died by 1902 |
| 3785 | Henty, G. A. (George Alfred) | In the Reign of Terror: The Adventures of a Westminster Boy |  | all contributors died by 1902 |
| 3429 | Henty, G. A. (George Alfred) | St. George for England |  | all contributors died by 1902 |
| 3674 | Henty, G. A. (George Alfred) | The Dragon and the Raven; Or, The Days of King Alfred |  | all contributors died by 1902 |
| 2805 | Henty, G. A. (George Alfred) | With Lee in Virginia: A Story of the American Civil War |  | all contributors died by 1902 |
| 4931 | Henty, G. A. (George Alfred) | Won By the Sword : a tale of the Thirty Years' War |  | all contributors died by 1902 |
| 2276 | Hogg, James | The Private Memoirs and Confessions of a Justified Sinner |  | all contributors died by 1835 |
| 942 | Hudson, W. H. (William Henry) | Green Mansions: A Romance of the Tropical Forest |  | all contributors died by 1922 |
| 135 | Hugo, Victor | Les Misérables |  | all contributors died by 1928 |
| 2610 | Hugo, Victor | Notre-Dame de Paris |  | all contributors died by 1928 |
| 1371 | Irving, Washington | Astoria; Or, Anecdotes of an Enterprise Beyond the Rocky Mountains |  | all contributors died by 1859 |
| 1190 | James, Henry | The Jolly Corner |  | all contributors died by 1916 |
| 1993 | Jerome, Jerome K. (Jerome Klapka) | Told After Supper |  | all contributors died by 1927 |
| 1860 | Kingsley, Charles | Westward Ho! Or, The Voyages and Adventures of Sir Amyas Leigh, Knight, of Burrough, in th |  | all contributors died by 1875 |
| 2735 | Kirby, William | The Golden Dog |  | all contributors died by 1906 |
| 467 | La Fayette, Madame de (Marie-Madeleine Pioche de L | The Princess of Cleves |  | all contributors died by 1693 |
| 128 | Lang, Andrew | The Arabian Nights Entertainments |  | all contributors died by 1912 |
| 503 | Lang, Andrew | The Blue Fairy Book |  | all contributors died by 1912 |
| 1036 | Lawson, Henry | Joe Wilson and His Mates |  | all contributors died by 1922 |
| 3732 | Lewis, Alfred Henry | Wolfville |  | all contributors died by 1914 |
| 3667 | Lewis, Alfred Henry | Wolfville Days |  | all contributors died by 1914 |
| 601 | Lewis, M. G. (Matthew Gregory) | The Monk: A Romance |  | all contributors died by 1818 |
| 4581 | Liljencrantz, Ottilie A. (Ottilia Adelina) | The Thrall of Leif the Lucky: A Story of Viking Days |  | all contributors died by 1910 |
| 501 | Lofting, Hugh | The Story of Doctor Dolittle | 1920 | front matter dated 1920 |
| 1154 | Lofting, Hugh | The Voyages of Doctor Dolittle | 1922 | front matter dated 1922 |
| 1163 | London, Jack | Adventure |  | all contributors died by 1916 |
| 310 | London, Jack | Before Adam |  | all contributors died by 1916 |
| 746 | London, Jack | Burning Daylight |  | all contributors died by 1916 |
| 1161 | London, Jack | Jerry of the Islands |  | all contributors died by 1916 |
| 2429 | London, Jack | Lost Face |  | all contributors died by 1916 |
| 710 | London, Jack | Love of Life, and Other Stories | 1907 | front matter dated 1907 |
| 1730 | London, Jack | Michael, Brother of Jerry |  | all contributors died by 1916 |
| 1596 | London, Jack | Smoke Bellew |  | all contributors died by 1916 |
| 1208 | London, Jack | South Sea Tales |  | all contributors died by 1916 |
| 911 | London, Jack | Tales of the Fish Patrol |  | all contributors died by 1916 |
| 1096 | London, Jack | The Faith of Men |  | all contributors died by 1916 |
| 2415 | London, Jack | The Mutiny of the Elsinore |  | all contributors died by 1916 |
| 788 | London, Jack | The Red One |  | all contributors died by 1916 |
| 1074 | London, Jack | The Sea-Wolf |  | all contributors died by 1916 |
| 2377 | London, Jack | The Son of the Wolf |  | all contributors died by 1916 |
| 215 | London, Jack | The call of the wild |  | all contributors died by 1916 |
| 2512 | London, Jack | The cruise of the Snark |  | all contributors died by 1916 |
| 910 | London, Jack | White Fang |  | all contributors died by 1916 |
| 1951 | Lytton, Edward Bulwer Lytton, Baron | The Coming Race |  | all contributors died by 1873 |
| 1565 | Lytton, Edward Bulwer Lytton, Baron | The Last Days of Pompeii |  | all contributors died by 1873 |
| 708 | MacDonald, George | The Princess and the Goblin |  | all contributors died by 1905 |
| 1412 | Marryat, Frederick | Masterman Ready |  | all contributors died by 1848 |
| 15 | Melville, Herman | Moby-Dick; or, The Whale |  | all contributors died by 1891 |
| 4045 | Melville, Herman | Omoo: Adventures in the South Seas |  | all contributors died by 1891 |
| 1900 | Melville, Herman | Typee: A Romance of the South Seas |  | all contributors died by 1908 |
| 4444 | Meredith, George | The Adventures of Harry Richmond — Volume 1 |  | all contributors died by 1909 |
| 4445 | Meredith, George | The Adventures of Harry Richmond — Volume 2 |  | all contributors died by 1909 |
| 4446 | Meredith, George | The Adventures of Harry Richmond — Volume 3 |  | all contributors died by 1909 |
| 4450 | Meredith, George | The Adventures of Harry Richmond — Volume 7 |  | all contributors died by 1909 |
| 4405 | Meredith, George | The Shaving of Shagpat; an Arabian entertainment — Complete |  | all contributors died by 1909 |
| 4443 | Meredith, George | Vittoria — Complete |  | all contributors died by 1909 |
| 3805 | Merriman, Henry Seton | The Vultures |  | all contributors died by 1903 |
| 357 | Morris, William | A Dream of John Ball; and, A King's Lesson |  | all contributors died by 1896 |
| 2565 | Morris, William | The Story of the Glittering Plain Which Has Been Also Called the Land of Living Men or the |  | all contributors died by 1896 |
| 169 | Morris, William | The Well at the World's End: A Tale |  | all contributors died by 1896 |
| 3055 | Morris, William | The Wood Beyond the World |  | all contributors died by 1896 |
| 4393 | Munroe, Kirk | Wakulla: a story of adventure in Florida |  | all contributors died by 1930 |
| 3942 | Musset, Alfred de | The Confession of a Child of the Century — Complete |  | all contributors died by 1857 |
| 3451 | Mühlbach, L. (Luise) | Marie Antoinette and Her Son |  | all contributors died by 1873 |
| 3536 | Nesbit, E. (Edith) | The Enchanted Castle |  | all contributors died by 1924 |
| 1874 | Nesbit, E. (Edith) | The Railway Children |  | all contributors died by 1924 |
| 837 | Nesbit, E. (Edith) | The Story of the Amulet |  | all contributors died by 1924 |
| 770 | Nesbit, E. (Edith) | The Story of the Treasure Seekers Being the Adventures of the Bastable Children in Search  |  | all contributors died by 1924 |
| 794 | Nesbit, E. (Edith) | The Wouldbegoods: Being the Further Adventures of the Treasure Seekers |  | all contributors died by 1924 |
| 321 | Norris, Frank | Moran of the Lady Letty |  | all contributors died by 1902 |
| 3465 | Ouida | Under Two Flags |  | all contributors died by 1908 |
| 4991 | Patchin, Frank Gee | The Pony Rider Boys in New Mexico; Or, The End of the Silver Trail |  | all contributors died by 1925 |
| 4057 | Pater, Walter | Marius the Epicurean — Volume 1 |  | all contributors died by 1894 |
| 4058 | Pater, Walter | Marius the Epicurean — Volume 2 |  | all contributors died by 1894 |
| 213 | Paterson, A. B. (Andrew Barton) | The Man from Snowy River | 1902 | front matter dated 1902 |
| 966 | Peacock, Thomas Love | Maid Marian |  | all contributors died by 1866 |
| 3703 | Pedley, Ethel C. | Dot and the Kangaroo |  | all contributors died by 1898 |
| 3497 | Perkins, Lucy Fitch | The Swiss Twins | 1922 | front matter dated 1922 |
| 4929 | Phillips, David Graham | The Fashionable Adventures of Joshua Craig: A Novel |  | all contributors died by 1911 |
| 932 | Poe, Edgar Allan | The Fall of the House of Usher |  | all contributors died by 1849 |
| 468 | Prévost, abbé | Manon Lescaut |  | all contributors died by 1763 |
| 973 | Pyle, Howard | Howard Pyle's Book of Pirates Fiction, Fact & Fancy Concerning the Buccaneers & Marooners  |  | all contributors died by 1911 |
| 1557 | Pyle, Howard | Men of Iron |  | all contributors died by 1911 |
| 964 | Pyle, Howard | The Merry Adventures of Robin Hood |  | all contributors died by 1911 |
| 3687 | Pyle, Howard | The Ruby of Kishmoor |  | all contributors died by 1911 |
| 3154 | Raspe, Rudolf Erich | The Surprising Adventures of Baron Munchausen |  | all contributors died by 1794 |
| 1366 | Reade, Charles | The Cloister and the Hearth |  | all contributors died by 1884 |
| 4912 | Richardson, Major (John) | Wacousta : a tale of the Pontiac conspiracy (Complete) |  | all contributors died by 1852 |
| 4994 | Rockwood, Roy | Five Thousand Miles Underground; Or, the Mystery of the Centre of the Earth | 1908 | front matter dated 1908 |
| 1194 | Rougemont, Louis de | The Adventures of Louis de Rougemont |  | all contributors died by 1921 |
| 1441 | Schreiner, Olive | The Story of an African Farm |  | all contributors died by 1920 |
| 1461 | Scott, Walter | A Legend of Montrose |  | all contributors died by 1832 |
| 2590 | Scott, Walter | Guy Mannering |  | all contributors died by 1832 |
| 82 | Scott, Walter | Ivanhoe: A Romance |  | all contributors died by 1832 |
| 1606 | Scott, Walter | Kenilworth |  | all contributors died by 1832 |
| 2516 | Scott, Walter | Redgauntlet: A Tale of the Eighteenth Century |  | all contributors died by 1832 |
| 1460 | Scott, Walter | The Black Dwarf |  | all contributors died by 1832 |
| 471 | Scott, Walter | The Bride of Lammermoor |  | all contributors died by 1832 |
| 1377 | Scott, Walter | The Talisman |  | all contributors died by 1832 |
| 1668 | Scott, Walter | The Tapestried Chamber, and Death of the Laird's Jock |  | all contributors died by 1832 |
| 4966 | Scott, Walter | Waverley; or, 'Tis sixty years since — Complete |  | all contributors died by 1832 |
| 259 | Service, Robert W. (Robert William) | Ballads of a Cheechako | 1909 | front matter dated 1909 |
| 271 | Sewell, Anna | Black Beauty |  | all contributors died by 1878 |
| 84 | Shelley, Mary Wollstonecraft | Frankenstein; or, The modern Prometheus |  | all contributors died by 1851 |
| 2853 | Sienkiewicz, Henryk | Quo Vadis: A Narrative of the Time of Nero |  | all contributors died by 1916 |
| 4084 | Smollett, T. (Tobias) | The Adventures of Peregrine Pickle |  | all contributors died by 1771 |
| 4085 | Smollett, T. (Tobias) | The Adventures of Roderick Random |  | all contributors died by 1771 |
| 3792 | Southworth, Emma Dorothy Eliza Nevitte | Capitola the madcap |  | all contributors died by 1899 |
| 589 | Stevenson, Robert Louis | Catriona |  | all contributors died by 1894 |
| 421 | Stevenson, Robert Louis | Kidnapped |  | all contributors died by 1894 |
| 839 | Stevenson, Robert Louis | New Arabian Nights |  | all contributors died by 1894 |
| 372 | Stevenson, Robert Louis | Prince Otto, a Romance |  | all contributors died by 1894 |
| 322 | Stevenson, Robert Louis | St. Ives: Being the Adventures of a French Prisoner in England |  | all contributors died by 1894 |
| 848 | Stevenson, Robert Louis | The Black Arrow: A Tale of the Two Roses |  | all contributors died by 1894 |
| 864 | Stevenson, Robert Louis | The Master of Ballantrae: A Winter's Tale |  | all contributors died by 1894 |
| 120 | Stevenson, Robert Louis | Treasure Island |  | all contributors died by 1926 |
| 3095 | Stoker, Bram | The Lady of the Shroud |  | all contributors died by 1912 |
| 1188 | Stoker, Bram | The Lair of the White Worm |  | all contributors died by 1912 |
| 2520 | Stoker, Bram | The Man |  | all contributors died by 1912 |
| 4995 | Stratemeyer, Edward | True to Himself; Or, Roger Strong's Struggle for Place |  | all contributors died by 1930 |
| 286 | Stratton-Porter, Gene | Laddie: A True Blue Story |  | all contributors died by 1924 |
| 3350 | Sue, Eugène | The Wandering Jew — Complete |  | all contributors died by 1857 |
| 829 | Swift, Jonathan | Gulliver's Travels into Several Remote Nations of the World |  | all contributors died by 1745 |
| 2511 | Thackeray, William Makepeace | The History of Henry Esmond, Esq., a Colonel in the Service of Her Majesty Queen Anne |  | all contributors died by 1863 |
| 4097 | Thompson, Maurice | Alice of Old Vincennes |  | all contributors died by 1901 |
| 3710 | Trollope, Anthony | An Unprotected Female at the Pyramids |  | all contributors died by 1882 |
| 1086 | Twain, Mark | A Horse's Tale |  | all contributors died by 1910 |
| 74 | Twain, Mark | The Adventures of Tom Sawyer, Complete |  | all contributors died by 1910 |
| 1837 | Twain, Mark | The Prince and the Pauper |  | all contributors died by 1910 |
| 91 | Twain, Mark | Tom Sawyer Abroad |  | all contributors died by 1910 |
| 3748 | Verne, Jules | A Journey into the Interior of the Earth |  | all contributors died by 1905 |
| 103 | Verne, Jules | Around the World in Eighty Days |  | all contributors died by 1905 |
| 3526 | Verne, Jules | Five Weeks in a Balloon Or, Journeys and Discoveries in Africa by Three Englishmen |  | all contributors died by 1905 |
| 2083 | Verne, Jules | In Search of the Castaways; Or, The Children of Captain Grant |  | all contributors died by 1905 |
| 1842 | Verne, Jules | Michael Strogoff; Or, The Courier of the Czar |  | all contributors died by 1905 |
| 1353 | Verne, Jules | Off on a Comet! a Journey through Planetary Space |  | all contributors died by 1905 |
| 3808 | Verne, Jules | Robur the Conqueror |  | all contributors died by 1905 |
| 3091 | Verne, Jules | The Giant Raft |  | all contributors died by 1905 |
| 3809 | Verne, Jules | The Master of the World |  | all contributors died by 1905 |
| 1268 | Verne, Jules | The Mysterious Island |  | all contributors died by 1913 |
| 1698 | Verne, Jules | The Survivors of the Chancellor |  | all contributors died by 1905 |
| 1355 | Verne, Jules | The Underground City; Or, The Black Indies (Sometimes Called The Child of the Cavern) |  | all contributors died by 1905 |
| 164 | Verne, Jules | Twenty Thousand Leagues under the Sea |  | all contributors died by 1905 |
| 3949 | Vigny, Alfred de | Cinq Mars — Volume 3 |  | all contributors died by 1863 |
| 2145 | Wallace, Lew | Ben-Hur: A tale of the Christ |  | all contributors died by 1905 |
| 696 | Walpole, Horace | The Castle of Otranto |  | all contributors died by 1894 |
| 3132 | Warner, Charles Dudley | In the Wilderness |  | all contributors died by 1900 |
| 1939 | Weyman, Stanley John | A Gentleman of France: Being the Memoirs of Gaston de Bonne Sieur de Marsac |  | all contributors died by 1928 |
| 2041 | Weyman, Stanley John | The House of the Wolf: A Romance |  | all contributors died by 1928 |
| 1896 | Weyman, Stanley John | Under the red robe |  | all contributors died by 1928 |
| 1033 | Wiggin, Kate Douglas Smith | Rose o' the River |  | all contributors died by 1923 |
| 174 | Wilde, Oscar | The Picture of Dorian Gray |  | all contributors died by 1900 |
| 4271 | Yonge, Charlotte M. (Charlotte Mary) | A Modern Telemachus |  | all contributors died by 1917 |
| 4538 | Yonge, Charlotte M. (Charlotte Mary) | Little Lucy's Wonderful Globe |  | all contributors died by 1901 |
| 3139 | Yonge, Charlotte M. (Charlotte Mary) | The Dove in the Eagle's Nest |  | all contributors died by 1901 |
| 2706 | Zschokke, Heinrich | The Bravo of Venice: A Romance |  | all contributors died by 1894 |

## crime (1429 books)

| Gutenberg ID | Author | Title | Year | PD basis |
|---|---|---|---|---|
| 59619 | A. L. O. E. | Beyond the Black Waters |  | all contributors died by 1893 |
| 2031 | Abbott, David P. (David Phelps); Carrington, Herew | The Lock and Key Library: The Most Interesting Stories of All Nations: Real Life | 1908 | front matter dated 1908 |
| 36335 | Adams, Samuel Hopkins | The Secret of Lonesome Cove | 1912 | front matter dated 1912 |
| 73001 | Agee, George W. (George Washington) | Rube Burrow, king of outlaws, and his band of train robbers |  | all contributors died by 1909 |
| 58940 | Aiken, Albert W. | The Wolf Demon; or, The Queen of the Kanawha |  | all contributors died by 1894 |
| 36481 | Ainsworth, William Harrison | Auriol; or, The Elixir of Life |  | all contributors died by 1882 |
| 16215 | Ainsworth, William Harrison | Jack Sheppard: A Romance |  | all contributors died by 1882 |
| 8188 | Alcott, Louisa May | The Mysterious Key and What It Opened |  | all contributors died by 1888 |
| 5435 | Aldrich, Thomas Bailey | The Stillwater Tragedy |  | all contributors died by 1907 |
| 5977 | Alger, Horatio, Jr. | Bound to Rise; Or, Up the Ladder |  | all contributors died by 1899 |
| 9990 | Alger, Horatio, Jr. | Brave and Bold; Or, The Fortunes of Robert Rushton |  | all contributors died by 1899 |
| 54294 | Alger, Horatio, Jr. | Charlie Codman's Cruise: A Story for Boys |  | all contributors died by 1899 |
| 53345 | Alger, Horatio, Jr. | Dan, the Newsboy |  | all contributors died by 1899 |
| 55947 | Alger, Horatio, Jr. | Dean Dunham; Or, the Waterford Mystery |  | all contributors died by 1899 |
| 21632 | Alger, Horatio, Jr. | Fame and Fortune; or, The Progress of Richard Hunter |  | all contributors died by 1899 |
| 528 | Alger, Horatio, Jr. | Joe the Hotel Boy; Or, Winning out by Pluck |  | all contributors died by 1899 |
| 26083 | Alger, Horatio, Jr. | Luke Walton |  | all contributors died by 1899 |
| 54608 | Alger, Horatio, Jr. | Ralph Raymond's Heir |  | all contributors died by 1899 |
| 55598 | Alger, Horatio, Jr. | Shifting For Himself; or, Gilbert Greyson's Fortunes |  | all contributors died by 1899 |
| 5417 | Alger, Horatio, Jr. | Struggling Upward, or Luke Larkin's Luck |  | all contributors died by 1899 |
| 54660 | Alger, Horatio, Jr. | The Disagreeable Woman: A Social Mystery |  | all contributors died by 1899 |
| 26075 | Alger, Horatio, Jr. | The Erie Train Boy |  | all contributors died by 1899 |
| 10724 | Alger, Horatio, Jr. | The Store Boy |  | all contributors died by 1899 |
| 55725 | Alger, Horatio, Jr. | The Train Boy |  | all contributors died by 1899 |
| 25150 | Alger, Horatio, Jr. | The Young Bank Messenger |  | all contributors died by 1899 |
| 4660 | Alger, Horatio, Jr. | Timothy Crump's Ward: A Story of American Life |  | all contributors died by 1899 |
| 56896 | Alger, Horatio, Jr. | Tom Thatcher's Fortune |  | all contributors died by 1899 |
| 59904 | Alger, Horatio, Jr. | Tony, the Hero; Or, A Brave Boy's Adventures with a Tramp |  | all contributors died by 1899 |
| 58304 | Alger, Horatio, Jr.; Stratemeyer, Edward | Falling in with Fortune; Or, The Experiences of a Young Secretary |  | all contributors died by 1930 |
| 25230 | Allan, Luke | The Return of Blue Pete | 1922 | front matter dated 1922 |
| 30970 | Allen, Grant | Miss Cayley's Adventures | 1899 | front matter dated 1899 |
| 5832 | Allen, Grant | Recalled to Life |  | all contributors died by 1899 |
| 38531 | Allen, Grant | The Beckoning Hand, and Other Stories |  | all contributors died by 1899 |
| 6010 | Allen, Grant | What's Bred in the Bone |  | all contributors died by 1899 |
| 4903 | Allen, Grant; Doyle, Arthur Conan | Hilda Wade, a Woman with Tenacity of Purpose |  | all contributors died by 1930 |
| 77537 | Allen, Ida Reade | Heart to heart | 1896 | front matter dated 1896 |
| 53607 | Anonymous | A Hoodoo Machine; or, The Motor Boys' Runabout No. 1313. | 1909 | front matter dated 1909 |
| 53602 | Anonymous | A Taxicab Tangle; or, The Mission of the Motor Boys | 1909 | front matter dated 1909 |
| 74548 | Anonymous | Great short stories, Volume 1 (of 3) | 1906 | front matter dated 1906 |
| 66900 | Anonymous | Life and Confession of Ann Walters, the Female Murderess!! Also the Execution of Enos G. D | 1849 | issue dated 1849 in the title |
| 77811 | Anonymous | Master tales of mystery, Volume 1 (of 3) | 1915 | front matter dated 1915 |
| 77812 | Anonymous | Master tales of mystery, Volume 2 (of 3) | 1915 | front matter dated 1915 |
| 27523 | Anonymous | Masterpieces of Mystery in Four Volumes: Detective Stories | 1920 | front matter dated 1920 |
| 27722 | Anonymous | Masterpieces of Mystery in Four Volumes: Ghost Stories | 1920 | front matter dated 1920 |
| 23432 | Anonymous | Masterpieces of Mystery in Four Volumes: Mystic-Humorous Stories | 1920 | front matter dated 1920 |
| 29704 | Anonymous | Masterpieces of Mystery in Four Volumes: Riddle Stories | 1920 | front matter dated 1920 |
| 54894 | Anonymous | Stephen H. Branch's Alligator, Vol. 1 no. 15, July 31, 1858 | 1858 | issue dated 1858 in the title |
| 16405 | Anonymous | Stories of Mystery | 1875 | front matter dated 1875 |
| 61003 | Anonymous | Stories of Tragedy | 1874 | front matter dated 1874 |
| 17893 | Anonymous | The Best Ghost Stories | 1919 | front matter dated 1919 |
| 46523 | Anonymous | The Spruce Street Tragedy; or, Old Spicer Handles a Double Mystery | 1887 | front matter dated 1887 |
| 52264 | Anonymous | Trial of William Palmer |  | all contributors died by 1924 |
| 53419 | Anonymous | Twenty-Five Ghost Stories | 1904 | front matter dated 1904 |
| 25043 | Anthony, Wilder | Hidden Gold | 1922 | front matter dated 1922 |
| 72659 | Appleton, Victor | Tom Swift and his chest of secrets | 1925 | front matter dated 1925 |
| 4588 | Arthur, T. S. (Timothy Shay) | The Allen House; Or, Twenty Years Ago and Now |  | all contributors died by 1885 |
| 39443 | Atherton, Gertrude Franklin Horn | Mrs. Balfame: A Novel | 1916 | front matter dated 1916 |
| 68507 | Badger, Jos. E. (Joseph Edward) | Redlaw, the half-breed; or, The tangled trail. A tale of the settlements |  | all contributors died by 1909 |
| 59653 | Bailey, H. C. (Henry Christopher) | Call Mr. Fortune | 1921 | front matter dated 1921 |
| 60096 | Bailey, H. C. (Henry Christopher) | Mr. Fortune's Practice | 1923 | front matter dated 1923 |
| 35822 | Baird, Jean K. (Jean Katherine) | That Little Girl of Miss Eliza's: A Story for Young People |  | all contributors died by 1918 |
| 48124 | Baker, Willard F. | Bob Dexter and the Storm Mountain Mystery; or, The Secret of the Log Cabin | 1925 | front matter dated 1925 |
| 27097 | Baker, Willard F. | The Boy Ranchers in Death Valley; Or, Diamond X and the Poison Mystery | 1928 | front matter dated 1928 |
| 79026 | Balfour, Hearnden | The enterprising burglar | 1928 | front matter dated 1928 |
| 29453 | Ball, Eustace Hale | Traffic in Souls: A Novel of Crime and Its Cure | 1914 | front matter dated 1914 |
| 15348 | Ballantyne, R. M. (Robert Michael) | Blown to Bits; or, The Lonely Man of Rakata |  | all contributors died by 1894 |
| 21737 | Ballantyne, R. M. (Robert Michael) | The Garret and the Garden; Or, Low Life High Up |  | all contributors died by 1894 |
| 21747 | Ballantyne, R. M. (Robert Michael) | The Lonely Island: The Refuge of the Mutineers |  | all contributors died by 1894 |
| 66114 | Balmer, Edwin | Keeban | 1923 | front matter dated 1923 |
| 75523 | Balmer, Edwin; MacHarg, William | The achievements of Luther Trant | 1910 | front matter dated 1910 |
| 1678 | Balzac, Honoré de | An Historical Mystery (The Gondreville Mystery) |  | all contributors died by 1908 |
| 1433 | Balzac, Honoré de | The Red Inn |  | all contributors died by 1908 |
| 30853 | Bangs, John Kendrick | Mrs. Raffles: Being the Adventures of an Amateur Crackswoman |  | all contributors died by 1929 |
| 20559 | Bangs, John Kendrick | R. Holmes & Co. Being the Remarkable Adventures of Raffles Holmes, Esq., Detective and Ama |  | all contributors died by 1922 |
| 3169 | Bangs, John Kendrick | The Pursuit of the House-Boat |  | all contributors died by 1922 |
| 21892 | Barbour, A. Maynard (Anna Maynard) | At the Time Appointed | 1903 | front matter dated 1903 |
| 72751 | Barbour, Ralph Henry; Holt, H. P. | The mystery of the Sea-Lark | 1920 | front matter dated 1920 |
| 73929 | Barclay, Vera C. (Vera Charlesworth) | Danny the detective | 1918 | front matter dated 1918 |
| 54901 | Baring-Gould, S. (Sabine) | Kitty Alone: A Story of Three Fires (vol. 3 of 3) |  | all contributors died by 1924 |
| 9312 | Barr, Robert | From Whose Bourne |  | all contributors died by 1912 |
| 9300 | Barr, Robert | Jennie Baxter, Journalist |  | all contributors died by 1912 |
| 8668 | Barr, Robert | Revenge! |  | all contributors died by 1912 |
| 8681 | Barr, Robert | The Face and the Mask |  | all contributors died by 1912 |
| 19369 | Barr, Robert | The Triumphs of Eugène Valmont |  | all contributors died by 1912 |
| 64386 | Barton, George | The Mystery of Cleverly: A Story for Boys | 1907 | front matter dated 1907 |
| 75068 | Barton, May Hollis | Three girl chums at Laurel Hall | 1926 | front matter dated 1926 |
| 5660 | Baum, L. Frank (Lyman Frank) | Mary Louise |  | all contributors died by 1919 |
| 24578 | Baum, L. Frank (Lyman Frank) | Mary Louise Solves a Mystery |  | all contributors died by 1919 |
| 45347 | Baum, L. Frank (Lyman Frank) | The Master Key An Electrical Fairy Tale Founded Upon the Mysteries of Electricity | 1901 | front matter dated 1901 |
| 34947 | Bayly, A. Eric | The House of Strange Secrets: A Detective Story | 1899 | front matter dated 1899 |
| 22109 | Beard, Daniel Carter | The Black Wolf Pack | 1922 | front matter dated 1922 |
| 39229 | Bedford-Jones, H. (Henry) | The Mardi Gras Mystery | 1920 | front matter dated 1920 |
| 63018 | Bedworth, Thomas | The Power of Conscience, exemplified in the genuine and extraordinary confession of Thomas | 1815 | issue dated 1815 in the title |
| 22706 | Bellamy, Edward | Two Days' Solitary Imprisonment 1898 |  | all contributors died by 1898 |
| 17495 | Bellinger, Martha Idell Fletcher | The Stolen Singer | 1911 | front matter dated 1911 |
| 75030 | Belloc, Hilaire | Mr. Petre | 1925 | front matter dated 1925 |
| 79269 | Belloc, Hilaire | The haunted house | 1928 | front matter dated 1928 |
| 57690 | Benson, E. F. (Edward Frederic) | The Luck of the Vails: A Novel | 1901 | front matter dated 1901 |
| 72421 | Benson, E. F. (Edward Frederic) | The room in the tower, and other stories | 1912 | front matter dated 1912 |
| 14275 | Benson, Robert Hugh | The Necromancers |  | all contributors died by 1914 |
| 21854 | Bentley, E. C. (Edmund Clerihew) | The Woman in Black | 1913 | front matter dated 1913 |
| 75476 | Berkeley, Anthony | The poisoned chocolates case | 1929 | front matter dated 1929 |
| 50177 | Besant, Walter | The Fourth Generation |  | all contributors died by 1901 |
| 34738 | Besant, Walter | The Ivory Gate, a new edition |  | all contributors died by 1901 |
| 24739 | Bidwell, Austin | Bidwell's Travels, from Wall Street to London Prison: Fifteen Years in Solitude | 1897 | front matter dated 1897 |
| 4387 | Bierce, Ambrose | Present at a Hanging and Other Ghost Stories |  | all contributors died by 1914 |
| 3715 | Bierce, Ambrose | The Parenticide Club |  | all contributors died by 1914 |
| 30836 | Biggers, Earl Derr | Seven Keys to Baldpate | 1913 | known first publication: first published 1913 |
| 73771 | Biggers, Earl Derr | The house without a key | 1925 | known first publication: first published 1925 |
| 56036 | Biggers, Earl Derr; Ritchie, Robert Welles | Inside the Lines | 1915 | front matter dated 1915 |
| 35823 | Bindloss, Harold | The Secret of the Reef | 1914 | front matter dated 1914 |
| 48237 | Binns, Ottwell | The Lady of North Star | 1922 | front matter dated 1922 |
| 21394 | Birmingham, George A. | Priscilla's Spies | 1912 | front matter dated 1912 |
| 41020 | Blackmore, R. D. (Richard Doddridge) | Clara Vaughan, Volume 1 (of 3) |  | all contributors died by 1900 |
| 41021 | Blackmore, R. D. (Richard Doddridge) | Clara Vaughan, Volume 2 (of 3) |  | all contributors died by 1900 |
| 41022 | Blackmore, R. D. (Richard Doddridge) | Clara Vaughan, Volume 3 (of 3) |  | all contributors died by 1900 |
| 45038 | Blackmore, R. D. (Richard Doddridge) | Perlycross: A Tale of the Western Hills |  | all contributors died by 1900 |
| 14471 | Blackwood, Algernon | The Empty House and Other Ghost Stories | 1916 | front matter dated 1916 |
| 52956 | Bloundelle-Burton, John | A Bitter Heritage: A Modern Story of Love and Adventure |  | all contributors died by 1917 |
| 69984 | Bly, Nellie | The mystery of Central Park |  | all contributors died by 1922 |
| 6658 | Bompas, Charlotte Selina | Owindia : a true tale of the MacKenzie River Indians, North-West America |  | all contributors died by 1917 |
| 35504 | Bonner, Geraldine | Miss Maitland, Private Secretary |  | all contributors died by 1930 |
| 35484 | Bonner, Geraldine | The Black Eagle Mystery | 1916 | front matter dated 1916 |
| 64934 | Bonner, Geraldine | The Castlecourt Diamond Mystery | 1905 | front matter dated 1905 |
| 35503 | Bonner, Geraldine | The Girl at Central | 1915 | front matter dated 1915 |
| 69322 | Bonner, Geraldine | The leading lady |  | all contributors died by 1930 |
| 9775 | Bonner, Geraldine | Treasure and Trouble Therewith: A Tale of California |  | all contributors died by 1930 |
| 21640 | Boothby, Guy | A Bid for Fortune; Or, Dr. Nikola's Vendetta |  | all contributors died by 1905 |
| 36118 | Boothby, Guy | A Crime of the Under-seas |  | all contributors died by 1928 |
| 54771 | Boothby, Guy | A Prince of Swindlers |  | all contributors died by 1905 |
| 10585 | Boothby, Guy | My Strangest Case |  | all contributors died by 1905 |
| 33610 | Boothby, Guy | Pharos, The Egyptian: A Romance |  | all contributors died by 1905 |
| 37948 | Boothby, Guy | The Beautiful White Devil |  | all contributors died by 1905 |
| 35277 | Boothby, Guy | The Childerbridge Mystery |  | all contributors died by 1905 |
| 42807 | Boothby, Guy | The Mystery of the Clasped Hands: A Novel |  | all contributors died by 1905 |
| 67822 | Bower, B. M. | The Ghost of One Man Coulee | 1913 | front matter dated 1913 |
| 72236 | Braddon, M. E. (Mary Elizabeth) | An open verdict |  | all contributors died by 1915 |
| 48021 | Braddon, M. E. (Mary Elizabeth) | Aurora Floyd, Vol. 2 Fifth Edition |  | all contributors died by 1915 |
| 48022 | Braddon, M. E. (Mary Elizabeth) | Aurora Floyd, Vol. 3 Fifth Edition |  | all contributors died by 1915 |
| 75125 | Braddon, M. E. (Mary Elizabeth) | Eleanor's victory |  | all contributors died by 1915 |
| 71631 | Braddon, M. E. (Mary Elizabeth) | His darling sin |  | all contributors died by 1915 |
| 8954 | Braddon, M. E. (Mary Elizabeth) | Lady Audley's Secret |  | all contributors died by 1915 |
| 75877 | Braddon, M. E. (Mary Elizabeth) | Lucius Davoren; or, Publicans and sinners, vol. 3 |  | all contributors died by 1915 |
| 17801 | Braddon, M. E. (Mary Elizabeth) | Milly Darrell |  | all contributors died by 1915 |
| 76927 | Braddon, M. E. (Mary Elizabeth) | Only a clod |  | all contributors died by 1915 |
| 9102 | Braddon, M. E. (Mary Elizabeth) | Run to Earth: A Novel |  | all contributors died by 1915 |
| 73931 | Braddon, M. E. (Mary Elizabeth) | The cloven foot |  | all contributors died by 1915 |
| 70938 | Braddon, M. E. (Mary Elizabeth) | The day will come |  | all contributors died by 1915 |
| 75840 | Braddon, M. E. (Mary Elizabeth) | The trail of the serpent |  | all contributors died by 1915 |
| 50037 | Braddon, M. E. (Mary Elizabeth) | Wyllard's Weird: A Novel |  | all contributors died by 1915 |
| 33476 | Braden, James A. (James Andrew) | The Auto Boys' Vacation | 1913 | front matter dated 1913 |
| 34732 | Bramah, Ernest | Max Carrados | 1914 | known first publication: collection, first published 1914 |
| 77788 | Bramah, Ernest | The eyes of Max Carrados | 1914 | known first publication: collection, first published 1914 |
| 12886 | Brame, Charlotte M. | The Coquette's Victim Everyday Life Library No. 1 |  | all contributors died by 1884 |
| 15183 | Brame, Charlotte M. | The Tragedy of the Chain Pier Everyday Life Library No. 3 |  | all contributors died by 1884 |
| 56992 | Branch, Stephen H. | Stephen H. Branch's Alligator, Vol. 1 no. 14, July 24, 1858 | 1858 | issue dated 1858 in the title |
| 34468 | Brebner, Percy James | Christopher Quarles: College Professor and Master Detective |  | all contributors died by 1922 |
| 9796 | Brebner, Percy James | The Master Detective: Being Some Further Investigations of Christopher Quarles |  | all contributors died by 1922 |
| 69955 | Brent, Henry Johnson | Was it a ghost? The murders in Bussey's wood |  | all contributors died by 1880 |
| 66916 | Bridges, Victor | Another Man's Shoes | 1913 | front matter dated 1913 |
| 66969 | Bridges, Victor | Greensea Island: A Mystery of the Essex Coast | 1921 | front matter dated 1921 |
| 67079 | Bridges, Victor | The Red Lodge: A Mystery of Campden Hill | 1924 | front matter dated 1924 |
| 69521 | Brown, Abbie Farwell | Surprise house | 1917 | front matter dated 1917 |
| 8223 | Brown, Charles Brockden | Edgar Huntly; or, Memoirs of a Sleep-Walker |  | all contributors died by 1810 |
| 76084 | Brownell, Gertrude Hall | The Nowadays Girls in the Adirondacks | 1915 | front matter dated 1915 |
| 57631 | Buchan, John | The Power-House | 1916 | front matter dated 1916 |
| 29331 | Burns, William J.; Ostrander, Isabel | The Crevice | 1915 | front matter dated 1915 |
| 331 | Burroughs, Edgar Rice | The Mucker | 1916 | front matter dated 1916 |
| 62409 | Burroughs, Edgar Rice | The girl from Hollywood | 1923 | front matter dated 1923 |
| 46774 | Burton, Frederick R. (Frederick Russell) | The Mission of Poubalov |  | all contributors died by 1909 |
| 29721 | Butler, Ellis Parker | Philo Gubb, Correspondence-School Detective | 1918 | front matter dated 1918 |
| 17937 | Butler, Ellis Parker | The Thin Santa Claus: The Chicken Yard That Was a Christmas Stocking | 1909 | front matter dated 1909 |
| 59892 | Byrne, Donn | Changeling, and Other Stories |  | all contributors died by 1928 |
| 33230 | Camp, Wadsworth | The Gray Mask | 1920 | front matter dated 1920 |
| 78435 | Campbell, Alice | Murder in Paris | 1930 | front matter dated 1930 |
| 68667 | Capes, Bernard | A rogue's tragedy |  | all contributors died by 1918 |
| 70105 | Capes, Bernard | Gilead Balm, knight errant |  | all contributors died by 1918 |
| 70048 | Capes, Bernard | The great Skene mystery |  | all contributors died by 1918 |
| 68688 | Capes, Bernard | The mill of silence |  | all contributors died by 1918 |
| 68712 | Capes, Bernard | The secret in the hill |  | all contributors died by 1918 |
| 61141 | Carling, John R. | The Weird Picture | 1905 | front matter dated 1905 |
| 24683 | Carr, Annie Roe | Nan Sherwood at Palm Beach; or, Strange adventures among the orange groves | 1921 | front matter dated 1921 |
| 55923 | Castlemon, Harry | Carl the Trailer |  | all contributors died by 1915 |
| 60407 | Castlemon, Harry | The Mystery of Lost River Canyon |  | all contributors died by 1915 |
| 6909 | Catherwood, Mary Hartwell | Old Caravan Days |  | all contributors died by 1902 |
| 59169 | Chadwick, Lester | Baseball Joe Saving the League; or, Breaking Up a Great Conspiracy | 1923 | front matter dated 1923 |
| 20445 | Chamberlain, Esther; Chamberlain, Lucia | The Coast of Chance | 1908 | front matter dated 1908 |
| 25724 | Chamberlain, Lucia | The Other Side of the Door | 1909 | front matter dated 1909 |
| 24306 | Chambers, Robert W. (Robert William) | The Flaming Jewel | 1922 | front matter dated 1922 |
| 52404 | Chambers, Robert W. (Robert William) | The Girl Philippa | 1916 | front matter dated 1916 |
| 46581 | Chambers, Robert W. (Robert William) | The Mystery of Choice | 1897 | front matter dated 1897 |
| 36313 | Champney, Elizabeth W. (Elizabeth Williams) | Witch Winnie's Mystery, or The Old Oak Cabinet: The Story of a King's Daughter | 1891 | front matter dated 1891 |
| 23005 | Chaplin, Heman White | Eli First published in the "Century Magazine" |  | all contributors died by 1924 |
| 38254 | Chapman, Allen | Bart Keene's Hunting Days; or, The Darewell Chums in a Winter Camp | 1911 | front matter dated 1911 |
| 37929 | Chapman, Allen | Fenn Masterson's Discovery; or, The Darewell Chums on a Cruise | 1909 | front matter dated 1909 |
| 38969 | Chapman, Allen | Ralph, the Train Dispatcher; Or, The Mystery of the Pay Car | 1911 | front matter dated 1911 |
| 44293 | Chapman, Allen | Tom Fairfield in Camp; or, The Secret of the Old Mill | 1913 | front matter dated 1913 |
| 30989 | Chapman, Arthur | Mystery Ranch | 1921 | front matter dated 1921 |
| 75998 | Charteris, Leslie | Daredevil | 1929 | front matter dated 1929 |
| 72869 | Charteris, Leslie | Meet the Tiger | 1928 | known first publication: first published 1928 |
| 53361 | Chase, Josephine | Patsy Carroll Under Southern Skies | 1918 | front matter dated 1918 |
| 73729 | Chekhov, Anton Pavlovich | The shooting party | 1926 | front matter dated 1926 |
| 37010 | Chester, George Randolph | Get-Rich-Quick Wallingford A Cheerful Account of the Rise and Fall of an American Business |  | all contributors died by 1924 |
| 32897 | Chester, George Randolph | Young Wallingford | 1910 | front matter dated 1910 |
| 1696 | Chesterton, G. K. (Gilbert Keith) | The Club of Queer Trades | 1905 | known first publication: first published 1905 |
| 1720 | Chesterton, G. K. (Gilbert Keith) | The Man Who Knew Too Much | 1922 | known first publication: first published 1922 |
| 1695 | Chesterton, G. K. (Gilbert Keith) | The Man Who Was Thursday: A Nightmare | 1908 | known first publication: first published 1908 |
| 204 | Chesterton, G. K. (Gilbert Keith) | The innocence of Father Brown | 1911 | known first publication: first published 1911 |
| 70175 | Chesterton, G. K. (Gilbert Keith) | The secret of Father Brown | 1927 | known first publication: first published 1927 |
| 223 | Chesterton, G. K. (Gilbert Keith) | The wisdom of Father Brown | 1914 | known first publication: first published 1914 |
| 57147 | Cheyney, Edward G. (Edward Gheen) | Scott Burton and the Timber Thieves | 1922 | front matter dated 1922 |
| 57194 | Cheyney, Edward G. (Edward Gheen) | Scott Burton on the Range | 1920 | front matter dated 1920 |
| 77022 | Chichester, John Jay | The porcelain mask | 1924 | front matter dated 1924 |
| 24451 | Child, Richard Washburn | The blue wall | 1912 | front matter dated 1912 |
| 2360 | Childers, Erskine | The Riddle of the Sands |  | all contributors died by 1922 |
| 19020 | Cholmondeley, Mary | The Danvers Jewels, and Sir Charles Danvers |  | all contributors died by 1925 |
| 78220 | Christie, Agatha | Murder at the vicarage | 1930 | known first publication: first published 1930 |
| 78342 | Christie, Agatha | Partners in crime | 1929 | known first publication: collection, first published 1929 |
| 61262 | Christie, Agatha | Poirot Investigates | 1924 | known first publication: collection, first published 1924 |
| 61168 | Christie, Agatha | The Man in the Brown Suit | 1924 | known first publication: first published 1924 |
| 58866 | Christie, Agatha | The Murder on the Links | 1923 | known first publication: first published 1923 |
| 863 | Christie, Agatha | The Mysterious Affair at Styles | 1920 | known first publication: first published 1920 |
| 1155 | Christie, Agatha | The Secret Adversary | 1922 | known first publication: first published 1922 |
| 65238 | Christie, Agatha | The Secret of Chimneys | 1925 | known first publication: first published 1925 |
| 69087 | Christie, Agatha | The murder of Roger Ackroyd | 1926 | known first publication: first published 1926 |
| 78084 | Christie, Agatha | The mysterious Mr. Quin | 1930 | known first publication: collection, first published 1930 |
| 72824 | Christie, Agatha | The mystery of the Blue Train | 1928 | known first publication: first published 1928 |
| 34058 | Claretie, Jules | The Crime of the Boulevard | 1897 | front matter dated 1897 |
| 71769 | Clay, Bertha M. | A tragedy of love and hate |  | all contributors died by 1922 |
| 78873 | Clendenen, Rufus Howard | Clendenen's detective manual | 1922 | front matter dated 1922 |
| 26306 | Clouston, J. Storer (Joseph Storer) | Simon | 1919 | front matter dated 1919 |
| 24799 | Cobb, Irvin S. (Irvin Shrewsbury) | The Escape of Mr. Trimm His Plight and other Plights | 1913 | front matter dated 1913 |
| 49860 | Cobb, Sylvanus | The Smuggler of King's Cove; or, The Old Chapel Mystery |  | all contributors died by 1887 |
| 13931 | Cobban, J. Maclaren (James Maclaren) | Master of His Fate |  | all contributors died by 1903 |
| 45245 | Cody, H. A. (Hiram Alfred) | The Long Patrol: A Tale of the Mounted Police | 1912 | front matter dated 1912 |
| 77231 | Cody, H. A. (Hiram Alfred) | The trail of the Golden Horn | 1923 | front matter dated 1923 |
| 78848 | Cohen, Octavus Roy | Jim Hanvey, detective | 1922 | front matter dated 1922 |
| 73716 | Cole, G. D. H. (George Douglas Howard) | The Brooklyn murders | 1924 | front matter dated 1924 |
| 79206 | Cole, G. D. H. (George Douglas Howard); Cole, Marg | The death of a millionaire | 1925 | front matter dated 1925 |
| 78883 | Cole, G. D. H. (George Douglas Howard); Cole, Marg | The man from the river | 1928 | front matter dated 1928 |
| 76634 | Collins, E. Burke, Mrs. | Lillian's vow |  | all contributors died by 1902 |
| 6738 | Collins, J. E. (Joseph Edmund) | The Four Canadian Highwaymen; Or, The Robbers of Markham Swamp |  | all contributors died by 1892 |
| 53145 | Collins, James H. (James Hiram) | The Great Taxicab Robbery: A True Detective Story | 1912 | front matter dated 1912 |
| 1629 | Collins, Wilkie | "I Say No" |  | all contributors died by 1889 |
| 1626 | Collins, Wilkie | After Dark |  | all contributors died by 1889 |
| 1895 | Collins, Wilkie | Armadale |  | all contributors died by 1889 |
| 1621 | Collins, Wilkie | Miss or Mrs.? |  | all contributors died by 1889 |
| 1628 | Collins, Wilkie | My Lady's Money |  | all contributors died by 1889 |
| 1587 | Collins, Wilkie | The Black Robe |  | all contributors died by 1889 |
| 7891 | Collins, Wilkie | The Dead Alive |  | all contributors died by 1889 |
| 1627 | Collins, Wilkie | The Evil Genius: A Domestic Story |  | all contributors died by 1889 |
| 3634 | Collins, Wilkie | The Guilty River |  | all contributors died by 1889 |
| 170 | Collins, Wilkie | The Haunted Hotel: A Mystery of Modern Venice |  | all contributors died by 1889 |
| 1622 | Collins, Wilkie | The Law and the Lady |  | all contributors died by 1889 |
| 1975 | Collins, Wilkie | The Legacy of Cain |  | all contributors died by 1889 |
| 155 | Collins, Wilkie | The Moonstone |  | all contributors died by 1889 |
| 1917 | Collins, Wilkie | The Queen of Hearts |  | all contributors died by 1889 |
| 583 | Collins, Wilkie | The Woman in White |  | all contributors died by 1889 |
| 7890 | Collins, Wilkie; Besant, Walter | Blind Love |  | all contributors died by 1901 |
| 73753 | Connington, J. J. | The Dangerfield Talisman | 1927 | front matter dated 1927 |
| 75407 | Connington, J. J. | Tragedy at Ravensthorpe | 1928 | front matter dated 1928 |
| 974 | Conrad, Joseph | The Secret Agent: A Simple Tale |  | all contributors died by 1924 |
| 43379 | Cook, D. J.‏ ‎(David J.) | Hands Up; or, Thirty-Five Years of Detective Life in the Mountains and on the Plains Remin |  | all contributors died by 1907 |
| 59847 | Coomes, Oll | Rainbolt, the Ranger; or, The Aerial Demon of the Mountain |  | all contributors died by 1921 |
| 70527 | Cooper, Courtney Ryley; Flynn, William J. (William | The Eagle's eye | 1919 | front matter dated 1919 |
| 75036 | Cooper, James Fenimore | The ways of the hour |  | all contributors died by 1851 |
| 70924 | Corbett, George, Mrs. | The adventures of Dora Bell, detective |  | all contributors died by 1930 |
| 62824 | Corbett, George, Mrs. | When the Sea Gives Up Its Dead: A Thrilling Detective Story |  | all contributors died by 1930 |
| 53097 | Corelli, Marie | The Murder of Delicia |  | all contributors died by 1924 |
| 45549 | Craine, E. J. (Edith Janice) | The Air Mystery of Isle La Motte | 1930 | front matter dated 1930 |
| 38123 | Crane, Laura Dent | The Automobile Girls at Palm Beach; Or, Proving Their Mettle Under Southern Skies | 1913 | front matter dated 1913 |
| 40844 | Crawford, F. Marion (Francis Marion) | The Diva's Ruby | 1908 | front matter dated 1908 |
| 10521 | Crawford, F. Marion (Francis Marion) | The Primadonna A Sequel to "Fair Margaret" |  | all contributors died by 1909 |
| 22246 | Crawford, F. Marion (Francis Marion) | The Upper Berth; By the Waters of Paradise |  | all contributors died by 1909 |
| 34017 | Crockett, S. R. (Samuel Rutherford) | Deep Moat Grange |  | all contributors died by 1914 |
| 65553 | Crofts, Freeman Wills | Inspector French's greatest case | 1925 | front matter dated 1925 |
| 75488 | Crofts, Freeman Wills | The purple sickle murders | 1929 | front matter dated 1929 |
| 29958 | Cullum, Ridgwell | The Law-Breakers | 1914 | front matter dated 1914 |
| 41145 | Cunningham, Francis | An account of the Death of Philip Jolin who was executed for the murder of his father, in  | 1829 | issue dated 1829 in the title |
| 25595 | Curties, Henry | A Queen's Error |  | all contributors died by 1928 |
| 4633 | Curwood, James Oliver | Philip Steele of the Royal Northwest Mounted Police |  | all contributors died by 1927 |
| 4702 | Curwood, James Oliver | The Flaming Forest |  | all contributors died by 1927 |
| 4515 | Curwood, James Oliver | The Golden Snare |  | all contributors died by 1927 |
| 4747 | Curwood, James Oliver | The River's End |  | all contributors died by 1927 |
| 29407 | Curwood, James Oliver | The Valley of Silent Men: A Story of the Three River Country |  | all contributors died by 1927 |
| 72803 | Dair, Spencer | Tracked to his lair; or, The pursuit of the Midnight Raider | 1910 | front matter dated 1910 |
| 33228 | Dallas, Richard | A master hand |  | all contributors died by 1924 |
| 59790 | Dana, Marvin | The Lake Mystery | 1923 | front matter dated 1923 |
| 54074 | Darrow, Clarence | An eye for an eye | 1905 | front matter dated 1905 |
| 5956 | Davis, Richard Harding | Gallegher and Other Stories |  | all contributors died by 1916 |
| 7884 | Davis, Richard Harding | In the Fog |  | all contributors died by 1916 |
| 11144 | Davis, Richard Harding | Somewhere in France |  | all contributors died by 1916 |
| 1822 | Davis, Richard Harding | The Amateur |  | all contributors died by 1916 |
| 1807 | Davis, Richard Harding | The Lost House |  | all contributors died by 1916 |
| 1818 | Davis, Richard Harding | The Spy |  | all contributors died by 1916 |
| 29400 | Dawson, Coningsby | Murder Point: A Tale of Keewatin | 1910 | front matter dated 1910 |
| 8572 | De Mille, James | Cord and Creese |  | all contributors died by 1880 |
| 6881 | De Quincey, Thomas | Note Book of an English Opium-Eater |  | all contributors died by 1859 |
| 370 | Defoe, Daniel | The Fortunes and Misfortunes of the Famous Moll Flanders |  | all contributors died by 1731 |
| 14065 | Defoe, Daniel | The History of the Remarkable Life of John Sheppard Containing a Particular Account of His |  | all contributors died by 1731 |
| 34934 | Delannoy, Burford | £19,000 | 1900 | front matter dated 1900 |
| 6917 | Dent, John Charles | The Gerrard Street Mystery and Other Weird Tales |  | all contributors died by 1888 |
| 917 | Dickens, Charles | Barnaby Rudge: A Tale of the Riots of 'Eighty |  | all contributors died by 1870 |
| 807 | Dickens, Charles | Hunted Down: The Detective Stories of Charles Dickens |  | all contributors died by 1870 |
| 730 | Dickens, Charles | Oliver Twist |  | all contributors died by 1870 |
| 564 | Dickens, Charles | The Mystery of Edwin Drood |  | all contributors died by 1870 |
| 924 | Dickens, Charles | To Be Read at Dusk |  | all contributors died by 1870 |
| 1423 | Dickens, Charles; Collins, Wilkie | No Thoroughfare |  | all contributors died by 1889 |
| 2324 | Dickens, Charles; Collins, Wilkie; Gaskell, Elizab | A House to Let |  | all contributors died by 1889 |
| 24702 | Dickey, Paul; Goddard, Charles | The Ghost Breaker: A Melodramatic Farce in Four Acts | 1909 | front matter dated 1909 |
| 72958 | Dixon, Franklin W. | Hunting for hidden gold | 1928 | front matter dated 1928 |
| 73102 | Dixon, Franklin W. | The Shore Road mystery | 1928 | front matter dated 1928 |
| 69988 | Dixon, Franklin W. | The house on the cliff | 1927 | front matter dated 1927 |
| 72840 | Dixon, Franklin W. | The missing chums | 1928 | front matter dated 1928 |
| 75012 | Dixon, Franklin W. | The mystery of Cabin Island | 1929 | front matter dated 1929 |
| 75310 | Dixon, Franklin W. | The secret of the caves | 1929 | front matter dated 1929 |
| 70236 | Dixon, Franklin W. | The secret of the old mill | 1927 | front matter dated 1927 |
| 70083 | Dixon, Franklin W. | The tower treasure | 1927 | front matter dated 1927 |
| 35819 | Dorrance, E. S. (Ethel Smith); Dorrance, James Fre | Lonesome Town | 1922 | front matter dated 1922 |
| 63877 | Dorrance, James French | Never Fire First: A Canadian Northwest Mounted Story | 1924 | front matter dated 1924 |
| 73900 | Dorrance, James French | The long arm of the Mounted | 1926 | front matter dated 1926 |
| 55189 | Dougall, L. (Lily) | The Summit House Mystery; Or, The Earthly Purgatory |  | all contributors died by 1923 |
| 37314 | Doughty, Francis Worcester | The Bradys After a Chinese Princess; Or, The Yellow Fiends of 'Frisco |  | all contributors died by 1917 |
| 26925 | Doughty, Francis Worcester | The Bradys Beyond Their Depth; Or, The Great Swamp Mystery |  | all contributors died by 1917 |
| 16919 | Doughty, Francis Worcester | The Bradys and the Girl Smuggler; Or, Working for the Custom House |  | all contributors died by 1917 |
| 37092 | Doughty, Francis Worcester | The Bradys' Chinese Clew; Or, The Secret Dens of Pell Street |  | all contributors died by 1917 |
| 60903 | Doughty, Francis Worcester | The Bradys' Race for Life; or, Rounding Up a Tough Trio: A Detective Story of Life |  | all contributors died by 1917 |
| 42750 | Dowling, Richard | Tempest-Driven: A Romance (Vol. 1 of 3) |  | all contributors died by 1898 |
| 42751 | Dowling, Richard | Tempest-Driven: A Romance (Vol. 2 of 3) |  | all contributors died by 1898 |
| 244 | Doyle, Arthur Conan | A Study in Scarlet |  | all contributors died by 1930 |
| 48320 | Doyle, Arthur Conan | Adventures of Sherlock Holmes Illustrated |  | all contributors died by 1930 |
| 22357 | Doyle, Arthur Conan | Danger! and Other Stories |  | all contributors died by 1930 |
| 2350 | Doyle, Arthur Conan | His last bow |  | all contributors died by 1930 |
| 69260 | Doyle, Arthur Conan | My friend the murderer, and other mysteries and adventures |  | all contributors died by 1930 |
| 66088 | Doyle, Arthur Conan | Recollections of Captain Wilkie: A Story of an Old Offender |  | all contributors died by 1930 |
| 54109 | Doyle, Arthur Conan | Round the Fire Stories |  | all contributors died by 1930 |
| 17398 | Doyle, Arthur Conan | The Cabman's Story The Mysteries of a London 'Growler' |  | all contributors died by 1930 |
| 13152 | Doyle, Arthur Conan | The Firm of Girdlestone |  | all contributors died by 1930 |
| 32777 | Doyle, Arthur Conan | The Great Keinplatz Experiment and Other Tales of Twilight and the Unseen |  | all contributors died by 1930 |
| 2852 | Doyle, Arthur Conan | The Hound of the Baskervilles |  | all contributors died by 1930 |
| 834 | Doyle, Arthur Conan | The Memoirs of Sherlock Holmes |  | all contributors died by 1930 |
| 355 | Doyle, Arthur Conan | The Parasite: A Story |  | all contributors died by 1930 |
| 108 | Doyle, Arthur Conan | The Return of Sherlock Holmes |  | all contributors died by 1930 |
| 3289 | Doyle, Arthur Conan | The Valley of Fear |  | all contributors died by 1930 |
| 69700 | Doyle, Arthur Conan | The case-book of Sherlock Holmes |  | all contributors died by 1930 |
| 7964 | Doyle, Arthur Conan | The mystery of Cloomber |  | all contributors died by 1930 |
| 75790 | Drake, H. B. (Henry Burgess) | Cursed be the treasure | 1928 | front matter dated 1928 |
| 75181 | Dreiser, Theodore | An American tragedy, v. 1 | 1925 | front matter dated 1925 |
| 75182 | Dreiser, Theodore | An American tragedy, v. 2 | 1925 | front matter dated 1925 |
| 53271 | Driscoll, James R. | The Brighton Boys at Chateau-Thierry | 1919 | front matter dated 1919 |
| 40491 | Du Boisgobey, Fortuné | The Red Lottery Ticket |  | all contributors died by 1891 |
| 45474 | DuPuy, William Atherton | Uncle Sam, Detective | 1916 | front matter dated 1916 |
| 16053 | Duchess | The Haunted Chamber: A Novel |  | all contributors died by 1897 |
| 2760 | Dumas, Alexandre | Celebrated Crimes (Complete) |  | all contributors died by 1870 |
| 75384 | Eberhart, Mignon G. (Mignon Good) | The patient in Room 18 | 1929 | front matter dated 1929 |
| 37707 | Edwards, Amelia B. | A Night on the Borders of the Black Forest |  | all contributors died by 1892 |
| 36112 | Edwards, Harry Stillwell | Sons and Fathers | 1921 | front matter dated 1921 |
| 77687 | Edwards, Leo | Jerry Todd and the rose-colored cat | 1924 | front matter dated 1924 |
| 71367 | Edwards, Leo | Poppy Ott and the galloping snail | 1927 | front matter dated 1927 |
| 75550 | Edwards, Leo | Poppy Ott and the stuttering parrot | 1926 | front matter dated 1926 |
| 71240 | Edwards, Leo | Poppy Ott's pedigreed pickles | 1927 | front matter dated 1927 |
| 12195 | Eggleston, Edward | The Mystery of Metropolisville |  | all contributors died by 1902 |
| 66051 | Eldridge, George Dyre | The Millbank Case: A Maine Mystery of To-day | 1905 | front matter dated 1905 |
| 63455 | Eliot, Ethel Cook | The Vanishing Comrade: A Mystery Story for Girls | 1924 | front matter dated 1924 |
| 25849 | Ellis, Edward Sylvester | The Launch Boys' Adventures in Northern Waters | 1912 | front matter dated 1912 |
| 41434 | Ellis, Edward Sylvester | The Launch Boys' Cruise in the Deerfoot | 1912 | front matter dated 1912 |
| 69168 | Ellis, Edward Sylvester | The phantom hunter; or, love after death |  | all contributors died by 1916 |
| 26613 | Emerson, Alice B. | Ruth Fielding At College; or, The Missing Examination Papers | 1917 | front matter dated 1917 |
| 23116 | Emerson, Alice B. | Ruth Fielding Down East; Or, The Hermit of Beach Plum Point | 1920 | front matter dated 1920 |
| 36747 | Emerson, Alice B. | Ruth Fielding Down in Dixie; Or, Great Times in the Land of Cotton | 1916 | front matter dated 1916 |
| 22743 | Emerson, Alice B. | Ruth Fielding and the Gypsies; Or, The Missing Pearl Necklace | 1915 | front matter dated 1915 |
| 29203 | Emerson, Alice B. | Ruth Fielding at Briarwood Hall; or, Solving the Campus Mystery | 1913 | front matter dated 1913 |
| 75509 | Endicott, Ruth Belmore | Carolyn of the sunny heart | 1919 | front matter dated 1919 |
| 23054 | Erckmann-Chatrian | The Dean's Watch | 1897 | front matter dated 1897 |
| 15258 | Falconer, Lanoe | Cecilia de Noël |  | all contributors died by 1908 |
| 45880 | Farjeon, B. L. (Benjamin Leopold) | A Secret Inheritance (Volume 1 of 3) |  | all contributors died by 1903 |
| 45881 | Farjeon, B. L. (Benjamin Leopold) | A Secret Inheritance (Volume 2 of 3) |  | all contributors died by 1903 |
| 45882 | Farjeon, B. L. (Benjamin Leopold) | A Secret Inheritance (Volume 3 of 3) |  | all contributors died by 1903 |
| 53044 | Farjeon, B. L. (Benjamin Leopold) | Devlin the Barber |  | all contributors died by 1903 |
| 42905 | Farjeon, B. L. (Benjamin Leopold) | Great Porter Square: A Mystery. v. 1 |  | all contributors died by 1903 |
| 42906 | Farjeon, B. L. (Benjamin Leopold) | Great Porter Square: A Mystery. v. 2 |  | all contributors died by 1903 |
| 42907 | Farjeon, B. L. (Benjamin Leopold) | Great Porter Square: A Mystery. v. 3 |  | all contributors died by 1903 |
| 43198 | Farjeon, B. L. (Benjamin Leopold) | Samuel Boyd of Catchpole Square: A Mystery |  | all contributors died by 1903 |
| 45525 | Farjeon, B. L. (Benjamin Leopold) | The Betrayal of John Fordham |  | all contributors died by 1903 |
| 42973 | Farjeon, B. L. (Benjamin Leopold) | The House of the White Shadows |  | all contributors died by 1903 |
| 43199 | Farjeon, B. L. (Benjamin Leopold) | The Last Tenant |  | all contributors died by 1903 |
| 53263 | Farjeon, B. L. (Benjamin Leopold) | The Mystery of M. Felix |  | all contributors died by 1903 |
| 53085 | Farjeon, B. L. (Benjamin Leopold) | The Nine of Hearts: A Novel |  | all contributors died by 1903 |
| 65709 | Farrère, Claude | The House of the Secret (La maison des hommes vivants) | 1923 | front matter dated 1923 |
| 46153 | Felix, Charles | The Notting Hill Mystery |  | all contributors died by 1903 |
| 67186 | Fellom, James | The rider of the Mohave | 1924 | front matter dated 1924 |
| 24871 | Fenn, George Manville | The Bag of Diamonds |  | all contributors died by 1909 |
| 25637 | Fenn, George Manville | The Dark House: A Knot Unravelled |  | all contributors died by 1909 |
| 34492 | Fenn, George Manville | The Master of the Ceremonies |  | all contributors died by 1909 |
| 34664 | Fenn, George Manville | The Mynns' Mystery |  | all contributors died by 1909 |
| 25607 | Fenn, George Manville | Witness to the Deed |  | all contributors died by 1909 |
| 79160 | Ferguson, J. A. (John Alexander) | The man in the dark | 1928 | front matter dated 1928 |
| 77438 | Ferguson, W. B. M. (William Blair Morton) | The Black Company | 1924 | front matter dated 1924 |
| 75146 | Fielding, A. (Archibald) | The Eames-Erskine case | 1925 | front matter dated 1925 |
| 5256 | Fielding, Henry | The History of the Life of the Late Mr. Jonathan Wild the Great |  | all contributors died by 1754 |
| 46437 | Finley, Martha | The Tragedy of Wild River Valley |  | all contributors died by 1909 |
| 19877 | Finnemore, John | Jack Haydon's Quest |  | all contributors died by 1915 |
| 31452 | Fitzhugh, Percy Keese | Roy Blakeley in the Haunted Camp | 1922 | front matter dated 1922 |
| 43011 | Fitzhugh, Percy Keese | Roy Blakeley's Silver Fox Patrol | 1920 | front matter dated 1920 |
| 72204 | Fitzhugh, Percy Keese | Tom Slade in the north woods | 1925 | front matter dated 1925 |
| 59439 | Fitzhugh, Percy Keese | Tom Slade on Overlook Mountain | 1923 | front matter dated 1923 |
| 46402 | Flanagan, T. J. | Harry Blount, the detective | 1891 | front matter dated 1891 |
| 22820 | Fleming, Brandon | The crooked house | 1921 | front matter dated 1921 |
| 35462 | Fleming, May Agnes | Sharing Her Crime: A Novel |  | all contributors died by 1880 |
| 72860 | Fleming, May Agnes | The queen of the isle |  | all contributors died by 1880 |
| 26324 | Fletcher, J. S. (Joseph Smith) | Ravensdene Court | 1922 | front matter dated 1922 |
| 20630 | Fletcher, J. S. (Joseph Smith) | The Borough Treasurer | 1921 | front matter dated 1921 |
| 27965 | Fletcher, J. S. (Joseph Smith) | The Chestermarke Instinct | 1921 | front matter dated 1921 |
| 25388 | Fletcher, J. S. (Joseph Smith) | The Herapath Property | 1921 | front matter dated 1921 |
| 59818 | Fletcher, J. S. (Joseph Smith) | The Markenmore Mystery | 1923 | front matter dated 1923 |
| 73344 | Fletcher, J. S. (Joseph Smith) | The copper box | 1923 | front matter dated 1923 |
| 79012 | Fletcher, J. S. (Joseph Smith) | The wolves and the lamb | 1925 | front matter dated 1925 |
| 75209 | Flynn, Brian | The case of the Black Twenty-Two | 1929 | front matter dated 1929 |
| 75195 | Flynn, Brian | The mystery of the Peacock's Eye | 1928 | front matter dated 1928 |
| 42010 | Flynn, William J. (William James) | The Barrel Mystery |  | all contributors died by 1928 |
| 57138 | Footner, Hulbert | Ramshackle House | 1922 | front matter dated 1922 |
| 31361 | Footner, Hulbert | The Deaves Affair | 1922 | front matter dated 1922 |
| 57088 | Footner, Hulbert | The Owl Taxi | 1921 | front matter dated 1921 |
| 57210 | Footner, Hulbert | The Substitute Millionaire | 1919 | front matter dated 1919 |
| 25875 | Footner, Hulbert | The Woman from Outside [On Swan River] | 1921 | front matter dated 1921 |
| 57236 | Footner, Hulbert | Thieves' Wit: An Everyday Detective Story | 1918 | front matter dated 1918 |
| 25333 | Ford, Paul Leicester | The Great K. & A. Robbery |  | all contributors died by 1902 |
| 13261 | Forman, Justus Miles | Jason: A Romance |  | all contributors died by 1915 |
| 78254 | Forrest, A. E. (Alfred Edgar) | Silent guests | 1927 | front matter dated 1927 |
| 46520 | Forrester, Andrew | Secret Service; or, Recollections of a City Detective |  | all contributors died by 1909 |
| 70233 | Fox-Davies, Arthur Charles | The duplicate death | 1910 | front matter dated 1910 |
| 2123 | France, Anatole | The Crime of Sylvestre Bonnard |  | all contributors died by 1924 |
| 72967 | Frank, Waldo David | Chalk face | 1924 | front matter dated 1924 |
| 33392 | Franklin, Edgar | In and Out | 1917 | front matter dated 1917 |
| 76812 | Franklin, Roy | Fighting for fortune | 1926 | front matter dated 1926 |
| 36854 | Franzos, Karl Emil | The Chief Justice: A Novel | 1884 | front matter dated 1884 |
| 298 | Frederic, Harold | The Market-Place |  | all contributors died by 1898 |
| 15695 | Freeman, Mary Eleanor Wilkins | 'Doc.' Gordon |  | all contributors died by 1930 |
| 1617 | Freeman, Mary Eleanor Wilkins | The Wind in the Rose-Bush, and Other Stories of the Supernatural |  | all contributors died by 1930 |
| 76796 | Freeman, R. Austin (Richard Austin) | A silent witness | 1929 | front matter dated 1929 |
| 24201 | Freeman, R. Austin (Richard Austin) | The Eye of Osiris | 1911 | front matter dated 1911 |
| 11128 | Freeman, R. Austin (Richard Austin) | The Red Thumb Mark | 1907 | known first publication: first published 1907 |
| 76116 | Freeman, R. Austin (Richard Austin) | The blue scarab | 1924 | front matter dated 1924 |
| 76072 | Freeman, R. Austin (Richard Austin) | The mystery of Angelina Frood | 1925 | front matter dated 1925 |
| 75244 | Freeman, R. Austin (Richard Austin) | The shadow of the Wolf | 1925 | front matter dated 1925 |
| 38983 | Frey, Hildegard G. | The Camp Fire Girls Solve a Mystery; Or, The Christmas Adventure at Carver House | 1919 | front matter dated 1919 |
| 22173 | Froest, Frank | The Grell Mystery | 1914 | front matter dated 1914 |
| 48821 | Frye, James A. (James Albert) | From Headquarters: Odd Tales Picked up in the Volunteer Service | 1892 | front matter dated 1892 |
| 58576 | Furlong, Thomas | Fifty Years a Detective: 35 Real Detective Stories | 1912 | front matter dated 1912 |
| 10943 | Futrelle, Jacques | Elusive Isabel |  | all contributors died by 1923 |
| 38981 | Futrelle, Jacques | The Chase of the Golden Plate | 1906 | front matter dated 1906 |
| 14896 | Futrelle, Jacques | The Diamond Master |  | all contributors died by 1912 |
| 37146 | Futrelle, Jacques | The Leak |  | all contributors died by 1912 |
| 547 | Gaboriau, Emile | Baron Trigault's Vengeance |  | all contributors died by 1873 |
| 2451 | Gaboriau, Emile | Caught in the Net |  | all contributors died by 1873 |
| 3803 | Gaboriau, Emile | File No. 113 |  | all contributors died by 1873 |
| 4071 | Gaboriau, Emile | Monsieur Lecoq, v. 1 |  | all contributors died by 1873 |
| 48641 | Gaboriau, Emile | Monsieur Lecoq, v. 2 |  | all contributors died by 1873 |
| 1748 | Gaboriau, Emile | Other People's Money |  | all contributors died by 1873 |
| 2736 | Gaboriau, Emile | The Champdoce Mystery |  | all contributors died by 1873 |
| 4604 | Gaboriau, Emile | The Clique of Gold |  | all contributors died by 1873 |
| 305 | Gaboriau, Emile | The Count's Millions |  | all contributors died by 1873 |
| 4002 | Gaboriau, Emile | The Honor of the Name |  | all contributors died by 1873 |
| 3802 | Gaboriau, Emile | The Lerouge Case |  | all contributors died by 1873 |
| 1651 | Gaboriau, Emile | The Mystery of Orcival |  | all contributors died by 1873 |
| 3336 | Gaboriau, Emile | Within an Inch of His Life |  | all contributors died by 1873 |
| 41137 | Gallon, Tom | Dead Man's Love |  | all contributors died by 1914 |
| 47271 | Gallon, Tom | The Second Dandy Chater |  | all contributors died by 1914 |
| 56743 | Garis, Howard Roger | Larry Dexter and the Stolen Boy; or, A Young Reporter on the Lakes | 1912 | front matter dated 1912 |
| 45497 | Garis, Lilian | Nancy Brandon | 1924 | front matter dated 1924 |
| 24879 | Gaskell, Elizabeth Cleghorn | Curious, if True Strange Tales |  | all contributors died by 1865 |
| 2153 | Gaskell, Elizabeth Cleghorn | Mary Barton |  | all contributors died by 1865 |
| 73520 | Gaul, Harriet A. (Harriet Avery) | Five nights at the Five Pines | 1922 | front matter dated 1922 |
| 47900 | Gibbs, George | The Splendid Outcast | 1920 | front matter dated 1920 |
| 55077 | Gibbs, George | The Yellow Dove | 1915 | front matter dated 1915 |
| 73838 | Gide, André | The Vatican swindle | 1925 | front matter dated 1925 |
| 75646 | Gillette, William | The astounding crime on Torrington Road | 1927 | front matter dated 1927 |
| 66859 | Gluck, Sinclair | Shadow in the House | 1929 | front matter dated 1929 |
| 73742 | Gluck, Sinclair | The house of the missing | 1922 | front matter dated 1922 |
| 1081 | Gogol, Nikolai Vasilevich | Dead Souls | 1842 | front matter dated 1842 |
| 58070 | Gogol, Nikolai Vasilevich | Home Life in Russia, Volumes 1 and 2 [Dead Souls] |  | all contributors died by 1866 |
| 69517 | Goldfrap, John Henry | The ocean wireless boys of the iceberg patrol | 1915 | front matter dated 1915 |
| 78776 | Goodchild, George | The monster of Grammont | 1930 | front matter dated 1930 |
| 51749 | Gordon, Frederick | Fairview Boys and Their Rivals; or, Bob Bouncer's Schooldays | 1912 | front matter dated 1912 |
| 52130 | Gordon, Frederick | Fairview Boys at Camp Mystery; or, the Old Hermit and His Secret | 1914 | front matter dated 1914 |
| 52143 | Gordon, Frederick | Fairview Boys at Lighthouse Cove; or, Carried out to Sea | 1914 | front matter dated 1914 |
| 75628 | Gorell, Ronald Gorell Barnes, Baron | In the night | 1917 | front matter dated 1917 |
| 35618 | Gould, Nat | Fast as the Wind: A Novel |  | all contributors died by 1919 |
| 33124 | Granice, Harry | Hunted Down; or, Five Days in the Fog A Thrilling Narrative of the Escape of Young Granice |  | all contributors died by 1915 |
| 69925 | Gratacap, L. P. (Louis Pope) | The new northland |  | all contributors died by 1927 |
| 36758 | Green, Anna Katharine | Cynthia Wakeham's Money | 1892 | front matter dated 1892 |
| 57643 | Green, Anna Katharine | Doctor Izard | 1895 | front matter dated 1895 |
| 33305 | Green, Anna Katharine | Lost Man's Lane: A Second Episode in the Life of Amelia Butterworth | 1898 | front matter dated 1898 |
| 34710 | Green, Anna Katharine | One of My Sons | 1901 | front matter dated 1901 |
| 31578 | Green, Anna Katharine | Room Number 3, and Other Detective Stories | 1913 | front matter dated 1913 |
| 21617 | Green, Anna Katharine | That Affair Next Door | 1897 | front matter dated 1897 |
| 22806 | Green, Anna Katharine | The Bronze Hand 1897 | 1897 | front matter dated 1897 |
| 17999 | Green, Anna Katharine | The Chief Legatee | 1906 | front matter dated 1906 |
| 23641 | Green, Anna Katharine | The Forsaken Inn: A Novel | 1909 | front matter dated 1909 |
| 22809 | Green, Anna Katharine | The Hermit Of ——— Street 1898 | 1898 | front matter dated 1898 |
| 4047 | Green, Anna Katharine | The Leavenworth Case | 1878 | known first publication: first published 1878 |
| 38347 | Green, Anna Katharine | The Millionaire Baby | 1905 | front matter dated 1905 |
| 17763 | Green, Anna Katharine | The Mystery of the Hasty Arrow | 1917 | front matter dated 1917 |
| 21824 | Green, Anna Katharine | The Old Stone House and Other Stories | 1891 | front matter dated 1891 |
| 33301 | Green, Anna Katharine | The Sword of Damocles: A Story of New York Life | 1881 | front matter dated 1881 |
| 68153 | Green, Anna Katharine | The step on the stair | 1923 | front matter dated 1923 |
| 32795 | Green, Anna Katharine | Three Thousand Dollars | 1909 | front matter dated 1909 |
| 14462 | Greene, Robert | The Third and Last Part of Conny-Catching. (1592) With the new deuised knauish arte of Foo |  | all contributors died by 1592 |
| 18950 | Gregory, Jackson | The Short Cut | 1916 | front matter dated 1916 |
| 16339 | Griffiths, Arthur | The Passenger from Calais |  | all contributors died by 1908 |
| 11451 | Griffiths, Arthur | The Rome Express |  | all contributors died by 1908 |
| 17434 | Griffiths, Arthur | The Thin Red Line; and Blue Blood |  | all contributors died by 1908 |
| 72378 | Grimshaw, Beatrice | The Sorcerer's Stone | 1914 | front matter dated 1914 |
| 62063 | Grove, Harriet Pyne | The Girls of Greycliff | 1923 | front matter dated 1923 |
| 11913 | Haggard, H. Rider (Henry Rider) | Mr. Meeson's Will |  | all contributors died by 1925 |
| 19695 | Hall, Angelo | Forty-one Thieves: A Tale of California |  | all contributors died by 1922 |
| 22221 | Hamilton, Levi Jackson | Oswald Langdon or, Pierre and Paul Lanier. A Romance of 1894-1898 | 1900 | front matter dated 1900 |
| 40605 | Hancock, H. Irving (Harrie Irving) | The Motor Boat Club at Nantucket; or, The Mystery of the Dunstan Heir |  | all contributors died by 1922 |
| 14369 | Hancock, H. Irving (Harrie Irving) | The Young Engineers on the Gulf Or, The Dread Mystery of the Million Dollar Breakwater |  | all contributors died by 1922 |
| 42802 | Hanshew, Mary E.; Hanshew, Thomas W. | The Riddle of the Mysterious Light | 1920 | front matter dated 1920 |
| 43135 | Hanshew, Mary E.; Hanshew, Thomas W. | The Riddle of the Purple Emperor | 1918 | front matter dated 1918 |
| 33279 | Hanshew, Mary E.; Hanshew, Thomas W. | The Riddle of the Spinning Wheel | 1922 | front matter dated 1922 |
| 32198 | Hanshew, Thomas W. | Cleek of Scotland Yard: Detective Stories |  | all contributors died by 1914 |
| 14332 | Hanshew, Thomas W. | Cleek: the Man of the Forty Faces |  | all contributors died by 1914 |
| 33271 | Hanshew, Thomas W. | The Riddle of the Night |  | all contributors died by 1914 |
| 45169 | Hapgood, Hutchins | The Autobiography of a Thief | 1903 | front matter dated 1903 |
| 66310 | Harbaugh, T. C. (Thomas Chalmers) | Silver Rifle, the Girl Trailer; Or, The White Tigers of Lake Superior |  | all contributors died by 1924 |
| 52702 | Harland, Henry | Mrs Peixada |  | all contributors died by 1905 |
| 43631 | Harland, Robert O. | The Vice Bondage of a Great City; or, the Wickedest City in the World | 1912 | front matter dated 1912 |
| 75325 | Hart, Frances Noyes | The Bellamy trial | 1927 | front matter dated 1927 |
| 2544 | Harte, Bret | From Sand Hill to Pine |  | all contributors died by 1902 |
| 15192 | Harte, Bret | Salomy Jane | 1910 | front matter dated 1910 |
| 41151 | Harvey, Marion | The Mystery of the Hidden Room | 1922 | front matter dated 1922 |
| 34988 | Hastings, Wells; Hooker, Brian | The Professor's Mystery | 1911 | front matter dated 1911 |
| 2181 | Hawthorne, Nathaniel | The Marble Faun; Or, The Romance of Monte Beni - Volume 1 |  | all contributors died by 1864 |
| 2182 | Hawthorne, Nathaniel | The Marble Faun; Or, The Romance of Monte Beni - Volume 2 |  | all contributors died by 1864 |
| 26396 | Hay, James | "No Clue!": A Mystery Story | 1920 | front matter dated 1920 |
| 20152 | Hay, James | The Winning Clue | 1919 | front matter dated 1919 |
| 75307 | Haynes, Annie | The Crow's Inn tragedy |  | all contributors died by 1929 |
| 59428 | Hecht, Ben | The Florentine Dagger: A Novel for Amateur Detectives | 1923 | front matter dated 1923 |
| 65834 | Heffernan, Dean L. | The Riders of Ramapo Pass | 1919 | front matter dated 1919 |
| 71506 | Henderley, Brooks | The Y. M. C. A. boys on Bass Island | 1916 | front matter dated 1916 |
| 79664 | Hendryx, James B. (James Beardsley) | Connie Morgan with the Mounted | 1918 | front matter dated 1918 |
| 35012 | Henty, G. A. (George Alfred) | A Search For A Secret: A Novel. Vol. 1 |  | all contributors died by 1902 |
| 35265 | Henty, G. A. (George Alfred) | A Search For A Secret: A Novel. Vol. 2 |  | all contributors died by 1902 |
| 35266 | Henty, G. A. (George Alfred) | A Search For A Secret: A Novel. Vol. 3 |  | all contributors died by 1902 |
| 8155 | Henty, G. A. (George Alfred) | Colonel Thorndyke's Secret |  | all contributors died by 1902 |
| 36103 | Henty, G. A. (George Alfred) | Dorothy's Double. Volume 1 (of 3) |  | all contributors died by 1902 |
| 36236 | Henty, G. A. (George Alfred) | Dorothy's Double. Volume 2 (of 3) |  | all contributors died by 1902 |
| 36975 | Henty, G. A. (George Alfred) | The Lost Heir |  | all contributors died by 1902 |
| 41791 | Herbert, A. P. (Alan Patrick) | The House by the River | 1921 | front matter dated 1921 |
| 40897 | Hering, Henry Augustus | The Burglars' Club: A Romance in Twelve Chronicles | 1905 | front matter dated 1905 |
| 59463 | Herrick, Robert | His Great Adventure | 1913 | front matter dated 1913 |
| 77428 | Hervey, Harry | The Black Parrot | 1923 | front matter dated 1923 |
| 66941 | Hicks, Albert W.; Fowler, L. N. (Lorenzo Niles) | The Life, Trial, Confession and Execution of Albert W. Hicks The Pirate and Murderer, Exec |  | all contributors died by 1896 |
| 32221 | Hill, Frederick Trevor | The Case and Exceptions: Stories of Counsel and Clients |  | all contributors died by 1930 |
| 38743 | Hill, Grace Brooks | The Corner House Girls How they moved to Milton, what they found, and what they did | 1915 | front matter dated 1915 |
| 62489 | Hill, Grace Brooks | The Corner House Girls Solve a Mystery What It Was, Where It Was, and Who Found It | 1923 | front matter dated 1923 |
| 14632 | Hill, Grace Livingston | The Mystery of Mary | 1912 | front matter dated 1912 |
| 69514 | Hill, Grace Livingston | The best man | 1914 | front matter dated 1914 |
| 33453 | Hill, Headon | A Traitor's Wooing |  | all contributors died by 1927 |
| 10832 | Hodgson, William Hope | Carnacki, the Ghost Finder |  | all contributors died by 1918 |
| 10966 | Hodgson, William Hope | The Ghost Pirates |  | all contributors died by 1918 |
| 10002 | Hodgson, William Hope | The House on the Borderland |  | all contributors died by 1918 |
| 40840 | Holbrook, James | Ten Years Among the Mail Bags Or, Notes from the Diary of a Special Agent of the Post-Offi |  | all contributors died by 1864 |
| 78323 | Holding, Elisabeth Sanxay | Dark power | 1930 | front matter dated 1930 |
| 46566 | Holt-White, W. (William) | The Crime Club | 1910 | front matter dated 1910 |
| 39547 | Hope, Anthony | Beaumaroy Home from the Wars | 1919 | front matter dated 1919 |
| 14623 | Hope, Laura Lee | Six little Bunkers at Grandma Bell's | 1918 | front matter dated 1918 |
| 73104 | Horniman, Roy | Israel Rank |  | all contributors died by 1930 |
| 33173 | Hornung, E. W. (Ernest William) | A Thief in the Night: Further adventures of A. J. Raffles, Cricketer and Cracksman |  | all contributors died by 1921 |
| 1703 | Hornung, E. W. (Ernest William) | Dead Men Tell No Tales |  | all contributors died by 1921 |
| 9806 | Hornung, E. W. (Ernest William) | Mr. Justice Raffles |  | all contributors died by 1921 |
| 11153 | Hornung, E. W. (Ernest William) | No Hero |  | all contributors died by 1921 |
| 707 | Hornung, E. W. (Ernest William) | Raffles: Further Adventures of the Amateur Cracksman |  | all contributors died by 1921 |
| 706 | Hornung, E. W. (Ernest William) | The Amateur Cracksman |  | all contributors died by 1921 |
| 30096 | Hornung, E. W. (Ernest William) | The Camera Fiend |  | all contributors died by 1921 |
| 37338 | Hornung, E. W. (Ernest William) | The Crime Doctor | 1914 | front matter dated 1914 |
| 12590 | Hornung, E. W. (Ernest William) | The Shadow of the Rope |  | all contributors died by 1921 |
| 37062 | Hornung, E. W. (Ernest William) | The Thousandth Woman | 1913 | front matter dated 1913 |
| 33971 | Hornung, E. W. (Ernest William) | Witching Hill |  | all contributors died by 1921 |
| 42902 | Hornung, E. W. (Ernest William) | Young Blood |  | all contributors died by 1921 |
| 45455 | Howard, Police Captain | Shadow, the Mysterious Detective | 1883 | front matter dated 1883 |
| 36237 | Howe, E. W. (Edgar Watson) | The Mystery of the Locks | 1885 | front matter dated 1885 |
| 24717 | Howe, William F.; Hummel, Abraham H. | Danger! A True History of a Great City's Wiles and Temptations The Veil Lifted, and Light  |  | all contributors died by 1926 |
| 69643 | Howitt, William | Woodburn Grange: A story of English country life; vol. 3 of 3 |  | all contributors died by 1879 |
| 26063 | Hume, Fergus | A Coin of Edward VII: A Detective Story | 1903 | front matter dated 1903 |
| 55457 | Hume, Fergus | A Creature of the Night: An Italian Enigma | 1891 | front matter dated 1891 |
| 56081 | Hume, Fergus | A Traitor in London | 1900 | front matter dated 1900 |
| 55420 | Hume, Fergus | For the Defence | 1898 | front matter dated 1898 |
| 23474 | Hume, Fergus | The Bishop's Secret | 1906 | front matter dated 1906 |
| 55305 | Hume, Fergus | The Black Patch | 1906 | front matter dated 1906 |
| 56841 | Hume, Fergus | The Disappearing Eye | 1908 | front matter dated 1908 |
| 56080 | Hume, Fergus | The Fever of Life | 1902 | front matter dated 1902 |
| 55310 | Hume, Fergus | The Lone Inn: A Mystery | 1895 | front matter dated 1895 |
| 55956 | Hume, Fergus | The Lost Parchment: A Detective Story | 1914 | front matter dated 1914 |
| 55137 | Hume, Fergus | The Mystery Queen | 1912 | front matter dated 1912 |
| 24769 | Hume, Fergus | The Opal Serpent | 1905 | front matter dated 1905 |
| 34835 | Hume, Fergus | The Pagan's Cup | 1902 | front matter dated 1902 |
| 55312 | Hume, Fergus | The Rainbow Feather | 1898 | front matter dated 1898 |
| 42056 | Hume, Fergus | The Red Window | 1904 | front matter dated 1904 |
| 55642 | Hume, Fergus | The Sacred Herb | 1908 | front matter dated 1908 |
| 55795 | Hume, Fergus | The Sealed Message | 1907 | front matter dated 1907 |
| 19069 | Hume, Fergus | The Silent House | 1907 | front matter dated 1907 |
| 43288 | Hume, Fergus | The Third Volume | 1895 | front matter dated 1895 |
| 54979 | Hume, Fergus | The Yellow Holly | 1903 | front matter dated 1903 |
| 32533 | Hunt, Henry M. | The Crime of the Century; Or, The Assassination of Dr. Patrick Henry Cronin | 1889 | front matter dated 1889 |
| 56720 | Hurlbut, Edward H. | Lanagan, Amateur Detective | 1913 | front matter dated 1913 |
| 64664 | Ingraham, Prentiss | Buffalo Bill's ruse |  | all contributors died by 1904 |
| 29792 | Ingraham, Prentiss | Buffalo Bill's spy trailer |  | all contributors died by 1904 |
| 43301 | Ingraham, Prentiss | Wizard Will, the wonder worker |  | all contributors died by 1904 |
| 35740 | Ingram, Eleanor M. (Eleanor Marie) | The Game and the Candle | 1909 | front matter dated 1909 |
| 23738 | Ingram, Eleanor M. (Eleanor Marie) | The Thing from the Lake |  | all contributors died by 1921 |
| 65811 | Ironside, John | The 'Phone Booth Mystery | 1924 | front matter dated 1924 |
| 31860 | Ironside, John | The Red Symbol | 1910 | front matter dated 1910 |
| 446 | Irving, H. B. (Henry Brodribb) | A Book of Remarkable Criminals |  | all contributors died by 1919 |
| 41790 | Jackson, Charles Ross | Quintus Oakes: A Detective Story |  | all contributors died by 1915 |
| 75967 | Jacques, Norbert | Dr. Mabuse, master of mystery | 1923 | front matter dated 1923 |
| 50856 | James, G. P. R. (George Payne Rainsford) | Charles Tyrrell; or, The Bitter Blood. Volumes I and II |  | all contributors died by 1860 |
| 42486 | James, Henry | The Two Magics: The Turn of the Screw, Covering End |  | all contributors died by 1916 |
| 34611 | Jarvis, Stinson | Geoffrey Hampstead: A Novel |  | all contributors died by 1926 |
| 37079 | Jefferies, Richard | World's End: A Story in Three Books |  | all contributors died by 1887 |
| 28084 | Jenkins, Herbert George | Malcolm Sage, Detective |  | all contributors died by 1923 |
| 37113 | Johnson, Owen | The Sixty-First Second | 1913 | front matter dated 1913 |
| 11240 | Johnston, William | The Apartment Next Door |  | all contributors died by 1929 |
| 27209 | Jones, Susan Morrow | The La Chance Mine Mystery | 1920 | front matter dated 1920 |
| 31471 | Jordan, Elizabeth Garver | The Girl in the Mirror | 1919 | front matter dated 1919 |
| 45866 | Kauffman, Reginald Wright | The Spider's Web | 1913 | front matter dated 1913 |
| 35964 | Kay, Ross | The Go Ahead Boys and the Mysterious Old House | 1916 | front matter dated 1916 |
| 35483 | Kay, Ross | The Go Ahead Boys on Smugglers' Island | 1916 | front matter dated 1916 |
| 78704 | Keene, Carolyn | The bungalow mystery | 1930 | front matter dated 1930 |
| 77602 | Keene, Carolyn | The hidden staircase | 1930 | front matter dated 1930 |
| 77873 | Keene, Carolyn | The mystery at Lilac Inn | 1930 | front matter dated 1930 |
| 77924 | Keene, Carolyn | The secret of the old clock | 1930 | front matter dated 1930 |
| 56718 | Kelland, Clarence Budington | Catty Atkins, Sailorman | 1922 | front matter dated 1922 |
| 72066 | Kelland, Clarence Budington | Contraband | 1923 | front matter dated 1923 |
| 16585 | Kelley, Francis Clement | Charred Wood | 1918 | front matter dated 1918 |
| 18309 | Kelly, Florence Finch | Emerson's Wife and Other Western Stories | 1911 | front matter dated 1911 |
| 41889 | Kendall, Ralph S. (Ralph Selwood) | Benton of the Royal Mounted: A Tale of the Royal Northwest Mounted Police | 1918 | front matter dated 1918 |
| 41525 | Kent, Elizabeth | The House Opposite: A Mystery | 1903 | front matter dated 1903 |
| 35205 | Kent, Elizabeth | Who? | 1912 | front matter dated 1912 |
| 72825 | Kernahan, Coulson | Captain Shannon | 1896 | front matter dated 1896 |
| 73740 | Kernahan, Coulson | The Dumpling | 1907 | front matter dated 1907 |
| 69024 | Kernahan, Coulson, Mrs. | The Thirteenth Man | 1910 | front matter dated 1910 |
| 64255 | King, Basil | The City of Comrades |  | all contributors died by 1928 |
| 16558 | King, Charles | From the Ranks | 1887 | front matter dated 1887 |
| 75500 | King, Rufus | Murder by the clock | 1929 | front matter dated 1929 |
| 38577 | Kummer, Frederic Arnold | The Blue Lights: A Detective Story | 1915 | front matter dated 1915 |
| 29498 | Kummer, Frederic Arnold | The Film of Fear | 1917 | front matter dated 1917 |
| 33019 | Kummer, Frederic Arnold | The Green God | 1911 | front matter dated 1911 |
| 29852 | Kummer, Frederic Arnold | The Ivory Snuff Box | 1912 | front matter dated 1912 |
| 79102 | Kästner, Erich | Emil and the detectives | 1929 | front matter dated 1929 |
| 37490 | Landon, Herman | The Gray Phantom's Return | 1922 | front matter dated 1922 |
| 76659 | Landon, Herman | The seventh shot | 1924 | front matter dated 1924 |
| 78010 | Landon, Herman | The unknown seven | 1923 | front matter dated 1923 |
| 18679 | Lang, Andrew | Historical Mysteries |  | all contributors died by 1912 |
| 21933 | Lang, Andrew | Much Darker Days |  | all contributors died by 1912 |
| 21821 | Lang, Andrew | The Mark of Cain |  | all contributors died by 1912 |
| 12345 | Lawson, Thomas William | Friday, the Thirteenth: A Novel | 1907 | front matter dated 1907 |
| 38460 | Le Fanu, Joseph Sheridan | Checkmate |  | all contributors died by 1873 |
| 41228 | Le Fanu, Joseph Sheridan | Guy Deverell, v. 1 of 2 |  | all contributors died by 1873 |
| 41229 | Le Fanu, Joseph Sheridan | Guy Deverell, v. 2 of 2 |  | all contributors died by 1873 |
| 37172 | Le Fanu, Joseph Sheridan | In a Glass Darkly, v. 1/3 |  | all contributors died by 1873 |
| 37174 | Le Fanu, Joseph Sheridan | In a Glass Darkly, v. 3/3 |  | all contributors died by 1873 |
| 11699 | Le Fanu, Joseph Sheridan | J. S. Le Fanu's Ghostly Tales, Volume 1 |  | all contributors died by 1873 |
| 11700 | Le Fanu, Joseph Sheridan | J. S. Le Fanu's Ghostly Tales, Volume 2 |  | all contributors died by 1873 |
| 11750 | Le Fanu, Joseph Sheridan | J. S. Le Fanu's Ghostly Tales, Volume 3 The Haunted Baronet (1871) |  | all contributors died by 1873 |
| 12592 | Le Fanu, Joseph Sheridan | J. S. Le Fanu's Ghostly Tales, Volume 5 |  | all contributors died by 1873 |
| 10377 | Le Fanu, Joseph Sheridan | The Evil Guest |  | all contributors died by 1873 |
| 17769 | Le Fanu, Joseph Sheridan | The House by the Church-Yard |  | all contributors died by 1873 |
| 509 | Le Fanu, Joseph Sheridan | The Purcell Papers — Volume 1 |  | all contributors died by 1873 |
| 9502 | Le Fanu, Joseph Sheridan | The Room in the Dragon Volant |  | all contributors died by 1873 |
| 35467 | Le Fanu, Joseph Sheridan | The Tenants of Malory, Volume 1 |  | all contributors died by 1873 |
| 35468 | Le Fanu, Joseph Sheridan | The Tenants of Malory, Volume 2 |  | all contributors died by 1873 |
| 35469 | Le Fanu, Joseph Sheridan | The Tenants of Malory, Volume 3 |  | all contributors died by 1873 |
| 40510 | Le Fanu, Joseph Sheridan | The Watcher, and other weird stories |  | all contributors died by 1929 |
| 68569 | Le Fanu, Joseph Sheridan | The Wyvern mystery |  | all contributors died by 1929 |
| 14851 | Le Fanu, Joseph Sheridan | Uncle Silas: A Tale of Bartram-Haugh |  | all contributors died by 1873 |
| 34662 | Le Fanu, Joseph Sheridan | Willing to Die: A Novel |  | all contributors died by 1873 |
| 9983 | Le Fanu, Joseph Sheridan | Wylder's Hand |  | all contributors died by 1873 |
| 26451 | Le Fanu, Joseph Sheridan; Young, Charles L. (Charl | A Stable for Nightmares; or, Weird Tales |  | all contributors died by 1887 |
| 72041 | Le Queux, William | A woman's debt |  | all contributors died by 1927 |
| 40997 | Le Queux, William | As We Forgive Them |  | all contributors died by 1927 |
| 73266 | Le Queux, William | Behind the bronze door | 1923 | front matter dated 1923 |
| 40829 | Le Queux, William | Devil's Dice |  | all contributors died by 1927 |
| 41456 | Le Queux, William | Guilty Bonds |  | all contributors died by 1927 |
| 41000 | Le Queux, William | Her Majesty's Minister |  | all contributors died by 1927 |
| 41093 | Le Queux, William | Her Royal Highness: A Romance of the Chancelleries of Europe |  | all contributors died by 1927 |
| 28337 | Le Queux, William | Hushed Up! A Mystery of London |  | all contributors died by 1927 |
| 4694 | Le Queux, William | Mademoiselle of Monte Carlo |  | all contributors died by 1927 |
| 41131 | Le Queux, William | Number 70, Berlin: A Story of Britain's Peril |  | all contributors died by 1927 |
| 77378 | Le Queux, William | Poison shadows |  | all contributors died by 1927 |
| 41186 | Le Queux, William | Sant of the Secret Service: Some Revelations of Spies and Spying |  | all contributors died by 1927 |
| 33298 | Le Queux, William | Spies of the Kaiser: Plotting the Downfall of England |  | all contributors died by 1927 |
| 41132 | Le Queux, William | The Bomb-Makers Being Some Curious Records Concerning the Craft and Cunning of Theodore Dr |  | all contributors died by 1927 |
| 41461 | Le Queux, William | The Bond of Black |  | all contributors died by 1927 |
| 41459 | Le Queux, William | The Broken Thread |  | all contributors died by 1927 |
| 40828 | Le Queux, William | The Closed Book: Concerning the Secret of the Borgias |  | all contributors died by 1927 |
| 30827 | Le Queux, William | The Count's Chauffeur |  | all contributors died by 1927 |
| 10102 | Le Queux, William | The Czar's Spy: The Mystery of a Silent Love |  | all contributors died by 1927 |
| 22654 | Le Queux, William | The Doctor of Pimlico: Being the Disclosure of a Great Crime |  | all contributors died by 1927 |
| 9795 | Le Queux, William | The Four Faces: A Mystery |  | all contributors died by 1927 |
| 41458 | Le Queux, William | The Gay Triangle: The Romance of the First Air Adventurers |  | all contributors died by 1927 |
| 27705 | Le Queux, William | The Golden Face: A Great 'Crook' Romance |  | all contributors died by 1927 |
| 41005 | Le Queux, William | The Great Court Scandal | 1890 | front matter dated 1890 |
| 41199 | Le Queux, William | The Great God Gold |  | all contributors died by 1927 |
| 10718 | Le Queux, William | The House of Whispers |  | all contributors died by 1927 |
| 41078 | Le Queux, William | The Hunchback of Westminster |  | all contributors died by 1927 |
| 41455 | Le Queux, William | The Lady in the Car |  | all contributors died by 1927 |
| 41454 | Le Queux, William | The Lost Million |  | all contributors died by 1927 |
| 41453 | Le Queux, William | The Mysterious Mr. Miller |  | all contributors died by 1927 |
| 40836 | Le Queux, William | The Mysterious Three |  | all contributors died by 1927 |
| 26637 | Le Queux, William | The Mystery of the Green Ray |  | all contributors died by 1927 |
| 40835 | Le Queux, William | The Pauper of Park Lane |  | all contributors died by 1927 |
| 40434 | Le Queux, William | The Place of Dragons: A Mystery |  | all contributors died by 1927 |
| 41001 | Le Queux, William | The Red Room |  | all contributors died by 1927 |
| 46236 | Le Queux, William | The Red Widow; or, The Death-Dealers of London |  | all contributors died by 1927 |
| 27549 | Le Queux, William | The Seven Secrets |  | all contributors died by 1927 |
| 30477 | Le Queux, William | The Sign of Silence |  | all contributors died by 1927 |
| 41089 | Le Queux, William | The Sign of the Stranger |  | all contributors died by 1927 |
| 41130 | Le Queux, William | The Stolen Statesman: Being the Story of a Hushed Up Mystery |  | all contributors died by 1927 |
| 27147 | Le Queux, William | The Stretton Street Affair |  | all contributors died by 1927 |
| 40833 | Le Queux, William | The Temptress |  | all contributors died by 1927 |
| 57885 | Le Queux, William | The Tickencote Treasure |  | all contributors died by 1927 |
| 41185 | Le Queux, William | The Voice from the Void: The Great Wireless Mystery |  | all contributors died by 1927 |
| 29173 | Le Queux, William | The White Lie |  | all contributors died by 1927 |
| 40831 | Le Queux, William | The Wiles of the Wicked |  | all contributors died by 1927 |
| 40995 | Le Queux, William | The Zeppelin Destroyer: Being Some Chapters of Secret History |  | all contributors died by 1927 |
| 78372 | Le Queux, William | The crime code |  | all contributors died by 1927 |
| 72870 | Le Queux, William | The crystal claw | 1924 | front matter dated 1924 |
| 78029 | Le Queux, William | The dangerous game | 1926 | front matter dated 1926 |
| 71037 | Le Queux, William | The gamblers |  | all contributors died by 1927 |
| 75760 | Le Queux, William | The house of evil |  | all contributors died by 1927 |
| 78884 | Le Queux, William | The looker-on |  | all contributors died by 1927 |
| 78920 | Le Queux, William | The money-spider |  | all contributors died by 1927 |
| 77737 | Le Queux, William | The rat trap |  | all contributors died by 1927 |
| 77530 | Le Queux, William | The sting |  | all contributors died by 1927 |
| 77426 | Le Queux, William | The three glass eyes |  | all contributors died by 1927 |
| 41187 | Le Queux, William | This House to Let |  | all contributors died by 1927 |
| 59434 | Le Queux, William | Tracked by Wireless |  | all contributors died by 1927 |
| 41092 | Le Queux, William | Whatsoever a Man Soweth |  | all contributors died by 1927 |
| 41184 | Le Queux, William | Whither Thou Goest |  | all contributors died by 1927 |
| 40837 | Le Queux, William | Whoso Findeth a Wife |  | all contributors died by 1927 |
| 39544 | Leahy, William Augustine | The Incendiary: A Story of Mystery | 1896 | front matter dated 1896 |
| 70413 | Lebhar, Bertram | The presidential snapshot | 1927 | front matter dated 1927 |
| 40203 | Leblanc, Maurice | Arsène Lupin versus Herlock Sholmes | 1910 | known first publication: English translation 1910 |
| 70719 | Leblanc, Maurice | Memoirs of Arsène Lupin | 1925 | front matter dated 1925 |
| 24839 | Leblanc, Maurice | The Blonde Lady Being a Record of the Duel of Wits between Arsène Lupin and the English De | 1910 | front matter dated 1910 |
| 28093 | Leblanc, Maurice | The Confessions of Arsène Lupin | 1912 | front matter dated 1912 |
| 28480 | Leblanc, Maurice | The Frontier | 1912 | front matter dated 1912 |
| 4017 | Leblanc, Maurice | The Hollow Needle; Further adventures of Arsène Lupin | 1910 | known first publication: English translation 1910 |
| 59072 | Leblanc, Maurice | The Secret Tomb | 1923 | front matter dated 1923 |
| 34939 | Leblanc, Maurice | The Secret of Sarek | 1920 | front matter dated 1920 |
| 34653 | Leblanc, Maurice | The Three Eyes | 1921 | front matter dated 1921 |
| 34931 | Leblanc, Maurice | The Woman of Mystery | 1916 | front matter dated 1916 |
| 46343 | Leroux, Gaston | The Man with the Black Feather | 1912 | front matter dated 1912 |
| 175 | Leroux, Gaston | The Phantom of the Opera |  | all contributors died by 1927 |
| 1686 | Leroux, Gaston | The Secret of the Night |  | all contributors died by 1927 |
| 76493 | Leroux, Gaston | The new terror | 1926 | front matter dated 1926 |
| 75258 | Leroux, Gaston | The perfume of the lady in black | 1909 | front matter dated 1909 |
| 69204 | Leverage, Henry | The white cipher | 1919 | front matter dated 1919 |
| 34046 | Leverage, Henry | Whispering Wires | 1918 | front matter dated 1918 |
| 51909 | Lewis, Alfred Henry | The Apaches of New York |  | all contributors died by 1914 |
| 66627 | Lincoln, Natalie Sumner | The Cat's Paw | 1922 | front matter dated 1922 |
| 24204 | Lincoln, Natalie Sumner | The Lost Despatch | 1913 | front matter dated 1913 |
| 63223 | Lincoln, Natalie Sumner | The Man Inside | 1914 | front matter dated 1914 |
| 58597 | Lincoln, Natalie Sumner | The Meredith Mystery | 1923 | front matter dated 1923 |
| 67890 | Lincoln, Natalie Sumner | The Thirteenth Letter | 1924 | front matter dated 1924 |
| 69004 | Lincoln, Natalie Sumner | The Trevor case | 1912 | front matter dated 1912 |
| 74210 | Lincoln, Natalie Sumner | The moving finger | 1918 | front matter dated 1918 |
| 68810 | Lincoln, Natalie Sumner | The nameless man | 1917 | front matter dated 1917 |
| 69388 | Lincoln, Natalie Sumner | The official chaperon | 1915 | front matter dated 1915 |
| 73597 | Lincoln, Natalie Sumner | The three strings | 1918 | front matter dated 1918 |
| 68679 | Lincoln, Natalie Sumner | The unseen ear | 1921 | front matter dated 1921 |
| 62760 | Lippard, George | The Mysteries of Florence |  | all contributors died by 1854 |
| 30450 | Livingston, Armstrong | The Monk of Hambleton | 1928 | front matter dated 1928 |
| 56015 | Locke, William John | Idols |  | all contributors died by 1930 |
| 23208 | Long, Helen Beecher | How Janice Day Won | 1917 | front matter dated 1917 |
| 56780 | Long, Lily A. (Lily Augusta) | The Hemlock Avenue Mystery |  | all contributors died by 1927 |
| 56961 | Long, Lily A. (Lily Augusta) | The Red House on Rowan Street | 1910 | front matter dated 1910 |
| 56838 | Long, Lily A. (Lily Augusta) | The Saintsbury Affair | 1912 | front matter dated 1912 |
| 17020 | Lorimer, George Horace | The False Gods | 1906 | front matter dated 1906 |
| 36079 | Lowndes, Marie Belloc | Love and hatred | 1917 | front matter dated 1917 |
| 70810 | Lowndes, Marie Belloc | The Terriford mystery | 1924 | front matter dated 1924 |
| 70698 | Lowndes, Marie Belloc | The lonely house | 1920 | front matter dated 1920 |
| 79259 | Lowndes, Marie Belloc | The story of Ivy | 1927 | front matter dated 1927 |
| 17381 | Lowndes, Marie Belloc | What Timmy Did | 1922 | front matter dated 1922 |
| 34208 | Lundsford, Hugh | The Law of Hemlock Mountain | 1920 | front matter dated 1920 |
| 38341 | Lyman, Olin L. (Olin Linus) | The Lash | 1909 | front matter dated 1909 |
| 36366 | Lynch, Lawrence L. | Dangerous Ground; or, The Rival Detectives | 1885 | front matter dated 1885 |
| 26482 | Lynch, Lawrence L. | Madeline Payne, the Detective's Daughter | 1884 | front matter dated 1884 |
| 38888 | Lynch, Lawrence L. | Out of a Labyrinth | 1885 | front matter dated 1885 |
| 25695 | Lynch, Lawrence L. | The Diamond Coterie | 1884 | front matter dated 1884 |
| 19472 | Lynde, Francis | Branded |  | all contributors died by 1930 |
| 67748 | Lynde, Francis | Scientific Sprague | 1912 | front matter dated 1912 |
| 34009 | Lynde, Francis | Stranded in Arcady | 1917 | front matter dated 1917 |
| 37249 | Lynde, Francis | The City of Numbered Days | 1914 | front matter dated 1914 |
| 19462 | Lynde, Francis | The Price |  | all contributors died by 1930 |
| 59621 | Lyons, Sophie | Why crime does not pay |  | all contributors died by 1924 |
| 7695 | Lytton, Edward Bulwer Lytton, Baron | A Strange Story — Volume 04 |  | all contributors died by 1873 |
| 7696 | Lytton, Edward Bulwer Lytton, Baron | A Strange Story — Volume 05 |  | all contributors died by 1873 |
| 7614 | Lytton, Edward Bulwer Lytton, Baron | Eugene Aram — Complete |  | all contributors died by 1873 |
| 7691 | Lytton, Edward Bulwer Lytton, Baron | Lucretia — Complete |  | all contributors died by 1873 |
| 7735 | Lytton, Edward Bulwer Lytton, Baron | Paul Clifford — Complete |  | all contributors died by 1873 |
| 7622 | Lytton, Edward Bulwer Lytton, Baron | Pelham — Volume 08 |  | all contributors died by 1873 |
| 7606 | Lytton, Edward Bulwer Lytton, Baron | Zicci: A Tale — Volume 01 |  | all contributors died by 1873 |
| 58711 | M'Govan, James | Traced and Tracked; Or, Memoirs of a City Detective |  | all contributors died by 1919 |
| 29877 | MacGowan, Alice; Newberry, Perry | The Million-Dollar Suitcase | 1922 | front matter dated 1922 |
| 17390 | MacGrath, Harold | Hearts and Masks | 1905 | front matter dated 1905 |
| 22158 | MacGrath, Harold | The Lure of the Mask | 1908 | front matter dated 1908 |
| 27339 | MacGrath, Harold | The Pagan Madonna | 1921 | front matter dated 1921 |
| 56945 | MacGrath, Harold | The Yellow Typhoon | 1919 | front matter dated 1919 |
| 39134 | MacGrath, Harold; Lonergan, F. | The Million Dollar Mystery Novelized from the Scenario of F. Lonergan | 1915 | front matter dated 1915 |
| 33064 | MacHarg, William; Balmer, Edwin | The Blind Man's Eyes | 1916 | front matter dated 1916 |
| 33065 | MacHarg, William; Balmer, Edwin | The Indian Drum | 1917 | front matter dated 1917 |
| 43298 | MacLaren, Gordon | The Riddle and the Ring; or, Won by Nerve | 1911 | front matter dated 1911 |
| 30647 | Macaulay, Rose | Mystery at Geneva: An Improbable Tale of Singular Happenings | 1922 | front matter dated 1922 |
| 24518 | Mackay, Charles | Memoirs of Extraordinary Popular Delusions and the Madness of Crowds |  | all contributors died by 1889 |
| 10029 | Magnay, William, Sir | The Hunt Ball Mystery |  | all contributors died by 1917 |
| 67703 | Magnay, William, Sir | The Master Spirit | 1906 | front matter dated 1906 |
| 58952 | Magnay, William, Sir | The Red Chancellor |  | all contributors died by 1917 |
| 3987 | Malot, Hector | Conscience — Volume 2 |  | all contributors died by 1907 |
| 46435 | Manning, Emmerson Wain | Practical Instruction for Detectives: A Complete Course in Secret Service Study | 1921 | front matter dated 1921 |
| 18965 | Marcin, Max | The Substitute Prisoner | 1911 | front matter dated 1911 |
| 75273 | Markham, Virgil | Death in the dusk | 1928 | front matter dated 1928 |
| 32401 | Marlowe, Amy Bell | The Girls of Hillcrest Farm; Or, The Secret of the Rocks | 1914 | front matter dated 1914 |
| 71328 | Marriott, Crittenden | Out of Russia | 1911 | front matter dated 1911 |
| 69217 | Marryat, Florence | The Hampstead mystery: a novel. Volume 2 (of 3) |  | all contributors died by 1899 |
| 21574 | Marryat, Frederick | The Poacher; Or, Joseph Rushbrook |  | all contributors died by 1848 |
| 38054 | Marsh, Richard | A Duel |  | all contributors died by 1915 |
| 38188 | Marsh, Richard | Amusement Only |  | all contributors died by 1915 |
| 79142 | Marsh, Richard | Judith Lee | 1912 | front matter dated 1912 |
| 37963 | Marsh, Richard | Miss Arnott's Marriage |  | all contributors died by 1915 |
| 5164 | Marsh, Richard | The Beetle: A Mystery |  | all contributors died by 1915 |
| 40349 | Marsh, Richard | The Chase of the Ruby |  | all contributors died by 1915 |
| 40347 | Marsh, Richard | The Coward Behind the Curtain |  | all contributors died by 1915 |
| 40353 | Marsh, Richard | The Datchet Diamonds |  | all contributors died by 1928 |
| 64997 | Marsh, Richard | The Joss: A Reversion |  | all contributors died by 1915 |
| 40452 | Marsh, Richard | The Twickenham Peerage |  | all contributors died by 1915 |
| 40449 | Marsh, Richard | The Woman with One Hand, and Mr. Ely's Engagement |  | all contributors died by 1928 |
| 64930 | Marsh, Richard | The goddess: a demon |  | all contributors died by 1915 |
| 33569 | Martin, Absalom | Kastle Krags: A Story of Mystery | 1921 | front matter dated 1921 |
| 76200 | Martin, Stuart | Only seven were hanged | 1929 | front matter dated 1929 |
| 40909 | Martyn, Wyndham | Anthony Trent, Master Criminal | 1918 | front matter dated 1918 |
| 40372 | Martyn, Wyndham | The Secret of the Silver Car Further Adventures of Anthony Trent, Master Criminal | 1920 | front matter dated 1920 |
| 40939 | Martyn, Wyndham; Megrue, Roi Cooper | Under Cover | 1914 | front matter dated 1914 |
| 38664 | Mason, A. E. W. (Alfred Edward Woodley) | The Four Corners of the World | 1917 | front matter dated 1917 |
| 67514 | Mason, A. E. W. (Alfred Edward Woodley) | The House of the Arrow | 1924 | front matter dated 1924 |
| 74782 | Mathers, Helen; À Beckett, Arthur William; Anstey, | The fate of Fenella | 1892 | front matter dated 1892 |
| 6569 | Mathews, Joanna H. (Joanna Hooe) | Bessie Bradford's Prize |  | all contributors died by 1901 |
| 46762 | Mathews, Joanna H. (Joanna Hooe) | Bessie and Her Friends |  | all contributors died by 1901 |
| 53533 | Matthews, Stanley R. | Motor Matt's Double Trouble; or, The Last of the Hoodoo | 1909 | front matter dated 1909 |
| 53390 | Matthews, Stanley R. | Motor Matt's Mandarin; or, Turning a Trick for Tsan Ti | 1909 | front matter dated 1909 |
| 53466 | Matthews, Stanley R. | Motor Matt's Mariner; or, Filling the Bill for Bunce | 1909 | front matter dated 1909 |
| 33829 | McConnell, Walter Caruth | The Nightriders' Feud | 1912 | front matter dated 1912 |
| 40484 | McCulley, Johnston | Black Star's Campaign: A Detective Story | 1919 | front matter dated 1919 |
| 35833 | McCulley, Johnston | The Black Star: A Detective Story | 1921 | front matter dated 1921 |
| 21891 | McCulley, Johnston | The Brand of Silence: A Detective Story | 1919 | front matter dated 1919 |
| 28229 | McCutcheon, George Barr | Anderson Crow, Detective |  | all contributors died by 1928 |
| 5871 | McCutcheon, George Barr | Green Fancy |  | all contributors died by 1928 |
| 6045 | McCutcheon, George Barr | The Hollow of Her Hand |  | all contributors died by 1928 |
| 54098 | McCutcheon, George Barr | The Light that Lies | 1916 | front matter dated 1916 |
| 5866 | McCutcheon, George Barr | Yollop |  | all contributors died by 1928 |
| 22781 | McGibeny, Donald | 32 Caliber | 1920 | front matter dated 1920 |
| 30838 | McIntyre, John T. (John Thomas) | Ashton-Kirk, Criminologist | 1918 | front matter dated 1918 |
| 39940 | McIntyre, John T. (John Thomas) | Ashton-Kirk, Secret Agent | 1912 | front matter dated 1912 |
| 67900 | McIntyre, John T. (John Thomas) | In the Dead of Night | 1908 | front matter dated 1908 |
| 66161 | McIntyre, John T. (John Thomas) | Special Detective (Ashton-Kirk) | 1922 | front matter dated 1922 |
| 61669 | McNeile, H. C. (Herman Cyril) | The Valley of the Shadow | 1924 | front matter dated 1924 |
| 66110 | Meade, L. T. | A Son of Ishmael: A Novel |  | all contributors died by 1914 |
| 20071 | Meade, L. T. | Sue, A Little Heroine |  | all contributors died by 1914 |
| 36361 | Mee, Huan | A Diplomatic Woman | 1900 | front matter dated 1900 |
| 26537 | Meigs, Cornelia | The Windy Hill | 1921 | front matter dated 1921 |
| 6701 | Meinhold, Wilhelm | Sidonia, the Sorceress : the Supposed Destroyer of the Whole Reigning Ducal House of Pomer |  | all contributors died by 1851 |
| 21816 | Melville, Herman | The Confidence-Man: His Masquerade |  | all contributors died by 1891 |
| 37949 | Merington, Marguerite | Scarlett of the Mounted | 1906 | front matter dated 1906 |
| 25799 | Merwin, Bannister | The Girl and the Bill An American Story of Mystery, Romance and Adventure | 1909 | front matter dated 1909 |
| 66203 | Meserve, Arthur L. (Arthur Livermore) | Death-Dealer, the Shawnee Scourge; or The Wizard of the Cliffs |  | all contributors died by 1896 |
| 62030 | Millet, Francis Davis | A Capillary Crime, and Other Stories |  | all contributors died by 1912 |
| 77431 | Mitchell, S. Weir (Silas Weir) | Constance Trescot |  | all contributors died by 1914 |
| 38169 | Mitford, Bertram | The Heath Hover Mystery |  | all contributors died by 1914 |
| 11373 | Moffett, Cleveland | Through the Wall |  | all contributors died by 1926 |
| 33922 | Moffett, Cleveland | True Detective Stories from the Archives of the Pinkertons |  | all contributors died by 1926 |
| 73472 | Moffett, Cleveland; Herford, Oliver | The Bishop's purse | 1913 | front matter dated 1913 |
| 31019 | Molesworth, Mrs. | Four Ghost Stories |  | all contributors died by 1921 |
| 35641 | Molesworth, Mrs. | Uncanny Tales |  | all contributors died by 1921 |
| 74441 | Morette, Edgar | The Sturgis wager | 1899 | front matter dated 1899 |
| 60978 | Morris, Charles | Will Somers, the Boy Detective |  | all contributors died by 1922 |
| 79666 | Morrison, Alexander | The Crookshaven murder | 1927 | front matter dated 1927 |
| 59319 | Morrison, Arthur | Adventures of Martin Hewitt, Third Series | 1896 | known first publication: collection, first published 1896 |
| 37820 | Morrison, Arthur | Chronicles of Martin Hewitt | 1895 | known first publication: collection, first published 1895 |
| 11252 | Morrison, Arthur | Martin Hewitt, Investigator | 1894 | known first publication: collection, first published 1894 |
| 53341 | Morrison, Arthur | The Dorrington Deed-Box | 1897 | known first publication: collection, first published 1897 |
| 64249 | Mudgett, Herman W. | Holmes' Own Story In Which the Alleged Multi-murderer and Arch Conspirator Tells of the Tw |  | all contributors died by 1896 |
| 33039 | Mulford, Clarence Edward | The Orphan | 1908 | front matter dated 1908 |
| 20057 | Munn, Charles Clark | Pocket Island: A Story of Country Life in New England |  | all contributors died by 1917 |
| 33787 | Munn, Charles Clark | Rockhaven |  | all contributors died by 1923 |
| 40321 | Nesbit, E. (Edith) | Grim Tales |  | all contributors died by 1924 |
| 33028 | Nesbit, E. (Edith) | Man and Maid |  | all contributors died by 1924 |
| 31426 | Newcomb, Ambrose | Eagles of the Sky; Or, With Jack Ralston Along the Air Lanes | 1930 | front matter dated 1930 |
| 45776 | Newcomb, Ambrose | The Sky Detectives; Or, How Jack Ralston Got His Man | 1930 | front matter dated 1930 |
| 45629 | Newcomb, Ambrose | The Sky Pilot's Great Chase; Or, Jack Ralston's Dead Stick Landing | 1930 | front matter dated 1930 |
| 45627 | Newcomb, Ambrose | Wings Over the Rockies; Or, Jack Ralston's New Cloud Chaser | 1930 | front matter dated 1930 |
| 67529 | Newton, W. Douglas (Wilfrid Douglas) | Double Crossed | 1922 | front matter dated 1922 |
| 15044 | Nicholson, Meredith | A Reversible Santa Claus | 1917 | front matter dated 1917 |
| 34512 | Nicholson, Meredith | Rosalind at Red Gate | 1907 | front matter dated 1907 |
| 13913 | Nicholson, Meredith | The Port of Missing Men | 1907 | front matter dated 1907 |
| 66974 | North, Grace May | Virginia's Ranch Neighbors | 1924 | front matter dated 1924 |
| 44401 | Norton, Carol | The Phantom Yacht | 1928 | front matter dated 1928 |
| 75583 | O'Flaherty, Liam | The informer | 1925 | front matter dated 1925 |
| 51848 | Oblinger, M. M. (Milo Milton) | Dick Kent at Half-Way House | 1929 | front matter dated 1929 |
| 15843 | Oemler, Marie Conway | Slippy McGee, Sometimes Known as the Butterfly Man | 1917 | front matter dated 1917 |
| 26175 | Old Sleuth | A Successful Shadow; Or, A Detective's Successful Quest |  | all contributors died by 1898 |
| 19929 | Old Sleuth | Cad Metti, The Female Detective Strategist; Or, Dudie Dunne Again in the Field |  | all contributors died by 1898 |
| 67179 | Old Sleuth | Nimble Ike, the Trick Ventriloquist: A Rousing Tale of Fun and Frolic |  | all contributors died by 1898 |
| 19335 | Old Sleuth | Oscar the Detective; Or, Dudie Dunne, The Exquisite Detective |  | all contributors died by 1898 |
| 5248 | Old Sleuth | The "Dock Rats" of New York; Or, The Smuggler Band's Last Stand |  | all contributors died by 1898 |
| 43765 | Old Sleuth | The Twin Ventriloquists; or, Nimble Ike and Jack the Juggler A Tale of Strategy and Juggle |  | all contributors died by 1898 |
| 26155 | Old Sleuth | Two Wonderful Detectives; Or, Jack and Gil's Marvelous Skill |  | all contributors died by 1898 |
| 61482 | Oliphant, Mrs. (Margaret) | The Mystery of Mrs. Blencarrow |  | all contributors died by 1897 |
| 55827 | Oliphant, Mrs. (Margaret) | Who Was Lost and Is Found: A Novel |  | all contributors died by 1897 |
| 43063 | Onions, Oliver | A Case in Camera | 1921 | front matter dated 1921 |
| 19341 | Oppenheim, E. Phillips (Edward Phillips) | A Maker of History | 1905 | front matter dated 1905 |
| 31535 | Oppenheim, E. Phillips (Edward Phillips) | A Monk of Cruta | 1894 | front matter dated 1894 |
| 30542 | Oppenheim, E. Phillips (Edward Phillips) | Berenice | 1911 | front matter dated 1911 |
| 32732 | Oppenheim, E. Phillips (Edward Phillips) | Jacob's Ladder | 1921 | front matter dated 1921 |
| 39018 | Oppenheim, E. Phillips (Edward Phillips) | Mr. Marx's Secret | 1916 | front matter dated 1916 |
| 35661 | Oppenheim, E. Phillips (Edward Phillips) | Mysterious Mr. Sabin | 1905 | front matter dated 1905 |
| 45636 | Oppenheim, E. Phillips (Edward Phillips) | Stolen Idols | 1925 | front matter dated 1925 |
| 17197 | Oppenheim, E. Phillips (Edward Phillips) | The Black Box | 1915 | front matter dated 1915 |
| 28091 | Oppenheim, E. Phillips (Edward Phillips) | The Double Four | 1917 | front matter dated 1917 |
| 34945 | Oppenheim, E. Phillips (Edward Phillips) | The Golden Web | 1911 | front matter dated 1911 |
| 5815 | Oppenheim, E. Phillips (Edward Phillips) | The Great Impersonation | 1920 | front matter dated 1920 |
| 34035 | Oppenheim, E. Phillips (Edward Phillips) | The Hillman | 1917 | front matter dated 1917 |
| 33546 | Oppenheim, E. Phillips (Edward Phillips) | The Missioner | 1909 | front matter dated 1909 |
| 30811 | Oppenheim, E. Phillips (Edward Phillips) | The Moving Finger | 1911 | front matter dated 1911 |
| 27998 | Oppenheim, E. Phillips (Edward Phillips) | The New Tenant | 1910 | front matter dated 1910 |
| 59198 | Oppenheim, E. Phillips (Edward Phillips) | The Seven Conundrums | 1923 | front matter dated 1923 |
| 35361 | Oppenheim, E. Phillips (Edward Phillips) | The Wicked Marquis | 1919 | front matter dated 1919 |
| 41402 | Oppenheim, E. Phillips (Edward Phillips) | The Yellow House; Master of Men | 1912 | front matter dated 1912 |
| 77836 | Oppenheim, E. Phillips (Edward Phillips) | The mystery road | 1923 | front matter dated 1923 |
| 33988 | Oppenheim, E. Phillips (Edward Phillips) | To Win the Love He Sought The Great Awakening: Volume 3 | 1912 | front matter dated 1912 |
| 32730 | Orczy, Emmuska Orczy, Baroness | The Heart of a Woman | 1911 | front matter dated 1911 |
| 75461 | Orczy, Emmuska Orczy, Baroness | The case of Miss Elliott | 1909 | front matter dated 1909 |
| 68172 | Orczy, Emmuska Orczy, Baroness | The man in grey Being episodes of the Chovan [i.e. Chouan] conspiracies in Normandy during | 1918 | front matter dated 1918 |
| 68237 | Orczy, Emmuska Orczy, Baroness | Unravelled Knots | 1924 | front matter dated 1924 |
| 36247 | Osborne, William Hamilton | The Red Mouse: A Mystery Romance | 1909 | front matter dated 1909 |
| 61840 | Osborne, William Hamilton | The Running Fight | 1910 | front matter dated 1910 |
| 72948 | Ostrander, Isabel | Annihilation |  | all contributors died by 1924 |
| 73155 | Ostrander, Isabel | Ashes to ashes |  | all contributors died by 1924 |
| 75240 | Ostrander, Isabel | Suspense |  | all contributors died by 1924 |
| 23885 | Ostrander, Isabel | The Fifth Ace | 1918 | front matter dated 1918 |
| 77423 | Ostrander, Isabel | The twenty-six clues |  | all contributors died by 1924 |
| 33242 | Otis, James | An Amateur Fireman |  | all contributors died by 1922 |
| 28697 | Otis, James | Down the Slope |  | all contributors died by 1912 |
| 32985 | Ottolengui, Rodrigues | A Modern Wizard | 1894 | front matter dated 1894 |
| 31915 | Ottolengui, Rodrigues | An Artist in Crime | 1892 | front matter dated 1892 |
| 35902 | Ottolengui, Rodrigues | Final Proof; Or, The Value of Evidence | 1898 | front matter dated 1898 |
| 23515 | Page, Thomas Nelson | The Spectre In The Cart 1908 |  | all contributors died by 1922 |
| 33814 | Paine, Albert Bigelow | The Mystery of Evelin Delorme: A Hypnotic Story | 1894 | front matter dated 1894 |
| 12357 | Parrish, Randall | The Case and the Girl |  | all contributors died by 1923 |
| 17647 | Parrish, Randall | The Strange Case of Cavendish |  | all contributors died by 1923 |
| 26657 | Paternoster, G. Sidney | The Motor Pirate |  | all contributors died by 1925 |
| 71516 | Paternoster, G. Sidney | The master criminal | 1907 | front matter dated 1907 |
| 37170 | Payn, James | Lost Sir Massingberd: A Romance of Real Life. v. 1/2 |  | all contributors died by 1898 |
| 37171 | Payn, James | Lost Sir Massingberd: A Romance of Real Life. v. 2/2 |  | all contributors died by 1898 |
| 35336 | Pemberton, Max | The Lady Evelyn: A Story of To-day | 1906 | front matter dated 1906 |
| 65489 | Pendexter, Hugh | It Might Have Happened Otherwise | 1915 | front matter dated 1915 |
| 54147 | Penrose, Margaret | Dorothy Dale and Her Chums | 1909 | front matter dated 1909 |
| 72644 | Penrose, Margaret | Dorothy Dale to the rescue | 1924 | front matter dated 1924 |
| 41558 | Penrose, Margaret | Dorothy Dale's Great Secret | 1909 | front matter dated 1909 |
| 39063 | Penrose, Margaret | The Motor Girls in the Mountains; or, The Gypsy Girl's Secret | 1919 | front matter dated 1919 |
| 25873 | Penrose, Margaret | The Motor Girls on Crystal Bay; or, The Secret of the Red Oar | 1914 | front matter dated 1914 |
| 61592 | Penrose, Margaret | The Radio Girls at Forest Lodge; or, The Strange Hut in the Swamp | 1924 | front matter dated 1924 |
| 71771 | Penrose, Margaret | The radio girls of Roselawn | 1922 | front matter dated 1922 |
| 431 | Phillips, David Graham | The Fortune Hunter |  | all contributors died by 1911 |
| 54795 | Phillpotts, Eden | The Poacher's Wife | 1906 | front matter dated 1906 |
| 20497 | Pinkerton, Allan | Bucholz and the Detectives |  | all contributors died by 1884 |
| 35686 | Pinkerton, Allan | Mississippi Outlaws and the Detectives Don Pedro and the Detectives; Poisoner and the Dete |  | all contributors died by 1884 |
| 22155 | Pinkerton, Allan | The Expressman and the Detective |  | all contributors died by 1884 |
| 30636 | Pinkerton, Allan | The Somnambulist and the Detective; The Murderer and the Fortune Teller |  | all contributors died by 1884 |
| 32007 | Pinkerton, Allan | The Spiritualists and the Detectives |  | all contributors died by 1884 |
| 65012 | Pirkis, Catherine Louisa | Disappeared From Her Home: A Novel |  | all contributors died by 1910 |
| 73377 | Pitts, J. R. S. (James Robert Soda) | Life and bloody career of the executed criminal, James Copeland, the great Southern land p |  | all contributors died by 1920 |
| 78103 | Poate, Ernest M. | The trouble at Pinelands | 1922 | front matter dated 1922 |
| 70400 | Pocock, Roger | The cheerful blackguard | 1915 | front matter dated 1915 |
| 78812 | Pont-Jest, René de | Shadowed by a detective |  | all contributors died by 1904 |
| 40416 | Porter, Rebecca N. (Rebecca Newman) | The Rest Hollow Mystery | 1922 | front matter dated 1922 |
| 51955 | Post, Melville Davisson | The Man of Last Resort; Or, The Clients of Randolph Mason |  | all contributors died by 1930 |
| 2861 | Post, Melville Davisson | The Sleuth of St. James's Square |  | all contributors died by 1930 |
| 51956 | Post, Melville Davisson | The Strange Schemes of Randolph Mason |  | all contributors died by 1930 |
| 62740 | Post, Melville Davisson | Walker of the Secret Service |  | all contributors died by 1930 |
| 60312 | Potter, Robert | The Germ Growers: An Australian story of adventure and mystery |  | all contributors died by 1908 |
| 78823 | Queen, Ellery | The French powder mystery | 1930 | front matter dated 1930 |
| 76339 | Queen, Ellery | The Roman hat mystery | 1929 | front matter dated 1929 |
| 17842 | Quiller-Couch, Arthur | Dead Man's Rock | 1894 | front matter dated 1894 |
| 3268 | Radcliffe, Ann Ward | The Mysteries of Udolpho |  | all contributors died by 1823 |
| 64701 | Radcliffe, Ann Ward | The Romance of the Forest, interspersed with some pieces of poetry. |  | all contributors died by 1823 |
| 26911 | Raine, William MacLeod | Crooked Trails and Straight | 1913 | front matter dated 1913 |
| 17066 | Raine, William MacLeod | Tangled Trails: A Western Detective Story | 1921 | front matter dated 1921 |
| 26540 | Ralphson, G. Harvey (George Harvey) | Boy Scouts in the Canal Zone; Or, The Plot Against Uncle Sam | 1911 | front matter dated 1911 |
| 31487 | Ralphson, G. Harvey (George Harvey) | Boy Scouts on the Great Divide; Or, The Ending of the Trail | 1913 | front matter dated 1913 |
| 62683 | Rathborne, St. George; Wrenn, Charles L. (Charles  | The Camp Fire Boys at Log Cabin Bend; Or, Four Chums Afoot in the Tall Timber | 1923 | front matter dated 1923 |
| 31655 | Raymond, Evelyn | A Daughter of the Forest |  | all contributors died by 1919 |
| 33853 | Raymond, Evelyn | Jessica Trent: Her Life on a Ranch |  | all contributors died by 1910 |
| 30074 | Raymond, Evelyn | Jessica, the Heiress |  | all contributors died by 1910 |
| 45492 | Raymond, P. T. | Bats in the Wall; or, The Mystery of Trinity Church-yard | 1892 | front matter dated 1892 |
| 12470 | Reade, Charles | A Perilous Secret |  | all contributors died by 1884 |
| 20546 | Rees, Arthur J. (Arthur John) | The Hand in the Dark | 1920 | front matter dated 1920 |
| 20494 | Rees, Arthur J. (Arthur John) | The Shrieking Pit | 1919 | front matter dated 1919 |
| 1923 | Reeve, Arthur B. (Arthur Benjamin) | The Poisoned Pen | 1911 | front matter dated 1911 |
| 33466 | Reeve, Arthur B. (Arthur Benjamin) | The Social Gangster | 1916 | front matter dated 1916 |
| 56902 | Reeve, Arthur B. (Arthur Benjamin) | The Soul Scar: A Craig Kennedy Scientific Mystery Novel | 1919 | front matter dated 1919 |
| 73414 | Reeve, Arthur B. (Arthur Benjamin) | The adventuress | 1917 | front matter dated 1917 |
| 16168 | Reeve, Arthur B. (Arthur Benjamin); Grey, John W. | The Master Mystery | 1919 | front matter dated 1919 |
| 52498 | Regis, Julius | No. 13 Toroni |  | all contributors died by 1925 |
| 76903 | Regis, Julius | The Copper House |  | all contributors died by 1925 |
| 35784 | Reid, Mayne | Gwen Wynn: A Romance of the Wye |  | all contributors died by 1883 |
| 35587 | Reid, Mayne | The Headless Horseman: A Strange Tale of Texas |  | all contributors died by 1883 |
| 47312 | Reynolds, George W. M. (George William MacArthur) | The Mysteries of London, v. 1/4 |  | all contributors died by 1879 |
| 51294 | Reynolds, George W. M. (George William MacArthur) | The Mysteries of London, v. 2/4 |  | all contributors died by 1879 |
| 52056 | Reynolds, George W. M. (George William MacArthur) | The Mysteries of London, v. 3/4 |  | all contributors died by 1879 |
| 51649 | Reynolds, George W. M. (George William MacArthur) | The Mysteries of London, v. 4/4 |  | all contributors died by 1879 |
| 5191 | Rhodes, W. H. (William Henry) | The Case of Summerfield |  | all contributors died by 1876 |
| 8602 | Riddell, J. H., Mrs. | The Uninhabited House |  | all contributors died by 1906 |
| 75909 | Ridley, Nat | The double dagger | 1926 | front matter dated 1926 |
| 54273 | Rinehart, Mary Roberts | Locked Doors | 1914 | front matter dated 1914 |
| 434 | Rinehart, Mary Roberts | The Circular Staircase | 1908 | known first publication: first published 1908 |
| 1869 | Rinehart, Mary Roberts | The Man in Lower Ten | 1909 | known first publication: first published 1909 |
| 75922 | Rinehart, Mary Roberts | The amazing adventures of Letitia Carberry | 1911 | front matter dated 1911 |
| 68950 | Rinehart, Mary Roberts | Twenty-three and a half hours' leave | 1918 | front matter dated 1918 |
| 35326 | Rives, Hallie Erminie | The Long Lane's Turning | 1917 | front matter dated 1917 |
| 41122 | Roberts, Theodore Goodridge | Rayton: A Backwoods Mystery | 1912 | front matter dated 1912 |
| 61911 | Roberts, Theodore Goodridge | The Oxbow Wizard | 1924 | front matter dated 1924 |
| 62768 | Roberts, Theodore Goodridge | The Red Pirogue: A Tale of Adventure in the Canadian Wilds | 1924 | front matter dated 1924 |
| 78094 | Roberts, Walter Adolphe | The haunting hand | 1926 | front matter dated 1926 |
| 42740 | Roche, Arthur Somers | Find the Woman | 1921 | front matter dated 1921 |
| 48655 | Rockwood, Roy | Dave Dashaway, Air Champion; Or, Wizard Work in the Clouds | 1915 | front matter dated 1915 |
| 41896 | Rockwood, Roy | Dave Fearless and the Cave of Mystery; or, Adrift on the Pacific | 1918 | front matter dated 1918 |
| 5320 | Roe, Edward Payson | Taken Alive |  | all contributors died by 1888 |
| 77001 | Rohmer, Sax | Moon of madness | 1927 | front matter dated 1927 |
| 77092 | Rohmer, Sax | She who sleeps | 1928 | front matter dated 1928 |
| 40108 | Rohmer, Sax | Tales of Secret Egypt | 1919 | front matter dated 1919 |
| 19142 | Rohmer, Sax | The Devil Doctor | 1916 | front matter dated 1916 |
| 15323 | Rohmer, Sax | The Green Eyes of Bâst | 1920 | front matter dated 1920 |
| 41619 | Rohmer, Sax | The Haunting of Low Fennel | 1924 | front matter dated 1924 |
| 21879 | Rohmer, Sax | The Sins of Séverac Bablon | 1914 | front matter dated 1914 |
| 79087 | Rohmer, Sax | The day the world ended | 1930 | front matter dated 1930 |
| 77056 | Rohmer, Sax | The dream detective | 1925 | front matter dated 1925 |
| 76621 | Rowe, John G. (John Gabriel) | Sergeant Dick of the Royal Mounted Police | 1929 | front matter dated 1929 |
| 76914 | Rudd, Stephen | The mystery of the missing eyebrows | 1921 | front matter dated 1921 |
| 61513 | Russell, William Clark | The Phantom Death, etc. |  | all contributors died by 1911 |
| 27475 | Ryan, Marah Ellis | That Girl Montana | 1901 | front matter dated 1901 |
| 48938 | Rymer, James Malcolm | Ada, the Betrayed; Or, The Murder at the Old Smithy. A Romance of Passion |  | all contributors died by 1884 |
| 59828 | Rymer, James Malcolm; Prest, Thomas Peckett | The String of Pearls; Or, The Barber of Fleet Street. A Domestic Romance. |  | all contributors died by 1884 |
| 59806 | Sackville-West, V. (Victoria) | The Dragon in Shallow Waters | 1922 | front matter dated 1922 |
| 54729 | Sadlier, Anna T. (Anna Theresa) | Wayward Winifred | 1905 | front matter dated 1905 |
| 29847 | Saltus, Edgar | The Paliser case |  | all contributors died by 1921 |
| 33207 | Saltus, Edgar | The Perfume of Eros: A Fifth Avenue Incident |  | all contributors died by 1921 |
| 60974 | Sampson, Emma Speed | Josie O'Gorman | 1923 | front matter dated 1923 |
| 64430 | Sampson, Emma Speed | Josie O'Gorman and the Meddlesome Major | 1924 | front matter dated 1924 |
| 22532 | Sampson, Emma Speed | Mary Louise and Josie O'Gorman | 1922 | front matter dated 1922 |
| 56831 | Saunders, Marshall | The King of the Park | 1897 | front matter dated 1897 |
| 6008 | Savage, Richard | The Midnight Passenger : A Novel |  | all contributors died by 1903 |
| 28271 | Sawyer, Ruth | Seven Miles to Arden | 1916 | front matter dated 1916 |
| 70432 | Sayers, Dorothy L. (Dorothy Leigh) | Clouds of witness | 1926 | known first publication: first published 1926 |
| 73295 | Sayers, Dorothy L. (Dorothy Leigh) | Lord Peter views the body | 1928 | known first publication: collection, first published 1928 |
| 78157 | Sayers, Dorothy L. (Dorothy Leigh) | Strong poison | 1930 | front matter dated 1930 |
| 72855 | Sayers, Dorothy L. (Dorothy Leigh) | The unpleasantness at the Bellona Club | 1928 | known first publication: first published 1928 |
| 70008 | Sayers, Dorothy L. (Dorothy Leigh) | Unnatural death | 1927 | known first publication: first published 1927 |
| 58820 | Sayers, Dorothy L. (Dorothy Leigh) | Whose Body? A Lord Peter Wimsey Novel | 1923 | known first publication: first published 1923 |
| 77601 | Sayers, Dorothy L. (Dorothy Leigh); Eustace, Rober | The documents in the case | 1930 | front matter dated 1930 |
| 25787 | Sayler, H. L. (Harry Lincoln) | On the Edge of the Arctic; Or, An Aeroplane in Snowland | 1913 | front matter dated 1913 |
| 6781 | Schiller, Friedrich | The Ghost-Seer; or the Apparitionist; and Sport of Destiny |  | all contributors died by 1805 |
| 27454 | Scott, John Reed | In Her Own Right | 1911 | front matter dated 1911 |
| 3321 | Scott, Leroy | Children of the Whirlwind |  | all contributors died by 1929 |
| 28820 | Scott, Leroy | Counsel for the Defense | 1911 | front matter dated 1911 |
| 71337 | Scott, Leroy | Mary Regan |  | all contributors died by 1929 |
| 50792 | Scott, Morgan | The Great Oakdale Mystery | 1912 | front matter dated 1912 |
| 6944 | Scott, Walter | The Heart of Mid-Lothian, Complete |  | all contributors died by 1832 |
| 56443 | Scott, Wellington | Seventeen Years in the Underworld | 1916 | front matter dated 1916 |
| 30905 | Seaman, Augusta Huiell | The Boarded-Up House | 1915 | front matter dated 1915 |
| 52509 | Seaman, Augusta Huiell | The Crimson Patch | 1919 | front matter dated 1919 |
| 25770 | Seaman, Augusta Huiell | The Dragon's Secret | 1920 | front matter dated 1920 |
| 39896 | Seaman, Augusta Huiell | The Girl Next Door | 1917 | front matter dated 1917 |
| 55964 | Seaman, Augusta Huiell | The Sapphire Signet | 1916 | front matter dated 1916 |
| 39900 | Seaman, Augusta Huiell | The Slipper Point Mystery | 1919 | front matter dated 1919 |
| 52946 | Seaman, Augusta Huiell | Three Sides of Paradise Green | 1918 | front matter dated 1918 |
| 78011 | Sheehan, Perley Poore | Three sevens | 1927 | front matter dated 1927 |
| 29524 | Sheldon, Georgie, Mrs. | The Masked Bridal |  | all contributors died by 1926 |
| 58022 | Sheldon, Lurana | My Queen: A Weekly Journal for Young Women. Issue 5, October 27, 1900 Marion Marlowe Entra | 1900 | issue dated 1900 in the title |
| 69037 | Sheppard, W. Crispin (William Crispin) | Don Hale Over There | 1918 | front matter dated 1918 |
| 67989 | Sheppard, W. Crispin (William Crispin) | The Rambler Club Afloat | 1909 | front matter dated 1909 |
| 71068 | Sheppard, W. Crispin (William Crispin) | The Rambler Club on the Texas border | 1915 | front matter dated 1915 |
| 68995 | Sheppard, W. Crispin (William Crispin) | The Rambler Club with the Northwest Mounted | 1914 | front matter dated 1914 |
| 67787 | Sheppard, W. Crispin (William Crispin) | The Rambler Club's Winter Camp | 1910 | front matter dated 1910 |
| 45136 | Sherman, Charles | He Comes Up Smiling | 1912 | front matter dated 1912 |
| 10709 | Shiel, M. P. (Matthew Phipps) | Prince Zaleski | 1895 | known first publication: collection, first published 1895 |
| 73914 | Shirley, Penn | The happy six |  | all contributors died by 1929 |
| 77243 | Sims, George R. (George Robert) | Dorcas Dene, detective |  | all contributors died by 1922 |
| 78210 | Sims, George R. (George Robert) | Dorcas Dene, detective |  | all contributors died by 1922 |
| 46443 | Sims, George R. (George Robert) | Rogues and Vagabonds |  | all contributors died by 1922 |
| 18563 | Sinclair, Bertrand W. | Raw gold | 1908 | front matter dated 1908 |
| 64609 | Sinclair, Upton | A West Point Treasure; Or, Mark Mallory's Strange Find | 1903 | front matter dated 1903 |
| 77835 | Siringo, Charles A. | A cowboy detective |  | all contributors died by 1928 |
| 73706 | Smith, Edward H. (Edward Henry) | Mysteries of the missing |  | all contributors died by 1927 |
| 28504 | Smith, Ruel Perley | The Rival Campers Ashore; or, The Mystery of the Mill | 1907 | front matter dated 1907 |
| 73110 | Snaith, J. C. (John Collis) | Henry Northcote | 1906 | front matter dated 1906 |
| 78222 | Snell, Edmund | The crimson butterfly | 1924 | front matter dated 1924 |
| 19351 | Snell, Roy J. (Roy Judson) | Curlie Carson Listens In | 1922 | front matter dated 1922 |
| 42728 | Snell, Roy J. (Roy Judson) | Forbidden Cargoes | 1927 | front matter dated 1927 |
| 45557 | Snell, Roy J. (Roy Judson) | Green Eyes | 1930 | front matter dated 1930 |
| 26372 | Snell, Roy J. (Roy Judson) | Panther Eye | 1921 | front matter dated 1921 |
| 43263 | Snell, Roy J. (Roy Judson) | The Arrow of Fire A Mystery Story for Boys | 1930 | front matter dated 1930 |
| 41721 | Snell, Roy J. (Roy Judson) | The Crimson Flash | 1922 | front matter dated 1922 |
| 41909 | Snell, Roy J. (Roy Judson) | The Crimson Thread: An Adventure Story for Girls | 1925 | front matter dated 1925 |
| 42040 | Snell, Roy J. (Roy Judson) | The Cruise of the O Moo | 1922 | front matter dated 1922 |
| 42755 | Snell, Roy J. (Roy Judson) | The Firebug | 1925 | front matter dated 1925 |
| 41837 | Snell, Roy J. (Roy Judson) | The Secret Mark An Adventure Story for Girls | 1923 | front matter dated 1923 |
| 41719 | Snell, Roy J. (Roy Judson) | White Fire | 1922 | front matter dated 1922 |
| 69675 | Southworth, Emma Dorothy Eliza Nevitte | Allworth Abbey |  | all contributors died by 1899 |
| 29029 | Souvestre, Pierre; Allain, Marcel | A Nest of Spies | 1917 | front matter dated 1917 |
| 27789 | Souvestre, Pierre; Allain, Marcel | A Royal Prisoner | 1918 | front matter dated 1918 |
| 28333 | Souvestre, Pierre; Allain, Marcel | Messengers of Evil Being a Further Account of the Lures and Devices of Fantômas | 1917 | front matter dated 1917 |
| 30586 | Souvestre, Pierre; Allain, Marcel | The Exploits of Juve Being the Second of the Series of the "Fantômas" Detective Tales | 1917 | front matter dated 1917 |
| 71587 | Souvestre, Pierre; Allain, Marcel | The long arm of Fantômas | 1924 | front matter dated 1924 |
| 46006 | Sparre, Christian | The Black Tortoise: Being the Strange Story of Old Frick's Diamond | 1901 | front matter dated 1901 |
| 29572 | Spearman, Frank H. (Frank Hamilton) | Whispering Smith | 1906 | front matter dated 1906 |
| 70512 | Speckman, Charles | The life, travels, exploits, frauds and robberies of Charles Speckman, alias Brown, who wa |  | all contributors died by 1763 |
| 57737 | Speight, T. W. (Thomas Wilkinson) | A Dead Reckoning |  | all contributors died by 1915 |
| 57946 | Speight, T. W. (Thomas Wilkinson) | In the Dead of Night: A Novel. Volume 2 (of 3) |  | all contributors died by 1915 |
| 57311 | Speight, T. W. (Thomas Wilkinson) | The Heart of a Mystery |  | all contributors died by 1915 |
| 57623 | Speight, T. W. (Thomas Wilkinson) | The Loudwater Tragedy |  | all contributors died by 1915 |
| 57755 | Speight, T. W. (Thomas Wilkinson) | The Mysteries of Heron Dyke: A Novel of Incident. Volume 1 (of 3) |  | all contributors died by 1915 |
| 57370 | Speight, T. W. (Thomas Wilkinson) | The Mysteries of Heron Dyke: A Novel of Incident. Volume 2 (of 3) |  | all contributors died by 1915 |
| 57415 | Speight, T. W. (Thomas Wilkinson) | The Mysteries of Heron Dyke: A Novel of Incident. Volume 3 (of 3) |  | all contributors died by 1915 |
| 57616 | Speight, T. W. (Thomas Wilkinson) | The Secret of Wyvern Towers |  | all contributors died by 1915 |
| 57294 | Speight, T. W. (Thomas Wilkinson) | Under Lock and Key: A Story. Volume 1 (of 3) |  | all contributors died by 1915 |
| 57295 | Speight, T. W. (Thomas Wilkinson) | Under Lock and Key: A Story. Volume 2 (of 3) |  | all contributors died by 1915 |
| 57296 | Speight, T. W. (Thomas Wilkinson) | Under Lock and Key: A Story. Volume 3 (of 3) |  | all contributors died by 1915 |
| 75070 | Sperry, Raymond | Larry Dexter and the bank mystery | 1912 | front matter dated 1912 |
| 77069 | Spewack, Samuel | Murder in the Gilded Cage | 1929 | front matter dated 1929 |
| 37357 | Stables, Gordon | Annie o' the Banks o' Dee |  | all contributors died by 1910 |
| 78643 | Stagg, Clinton H. (Clinton Holland) | Thornley Colton |  | all contributors died by 1916 |
| 41827 | Standish, Burt L. | Dick Merriwell Abroad; Or, The Ban of the Terrible Ten | 1904 | front matter dated 1904 |
| 41879 | Standish, Burt L. | Dick Merriwell's Pranks; Or, Lively Times in the Orient | 1905 | front matter dated 1905 |
| 41866 | Standish, Burt L. | Dick Merriwell's Trap; Or, The Chap Who Bungled | 1902 | front matter dated 1902 |
| 63815 | Standish, Burt L. | Frank Merriwell on the Road; Or, The All-Star Combination | 1905 | front matter dated 1905 |
| 22571 | Standish, Burt L. | Frank Merriwell's Bravery | 1903 | front matter dated 1903 |
| 34100 | Standish, Burt L. | Lefty Locke, pitcher-manager | 1916 | front matter dated 1916 |
| 65608 | Stark, Inspector | The Great Green Diamond; Or, Thief Against Thief | 1906 | front matter dated 1906 |
| 74974 | Steele, Harwood | Spirit-of-iron (Manitou-pewabic) | 1923 | front matter dated 1923 |
| 19523 | Steele, Jack | A Husband by Proxy | 1909 | front matter dated 1909 |
| 9185 | Stephens, Robert Neilson | The Mystery of Murray Davenport: A Story of New York at the Present Day |  | all contributors died by 1906 |
| 40433 | Stevens, Augusta de Grasse | Miss Hildreth: A Novel, Volume 3 |  | all contributors died by 1894 |
| 35247 | Stevenson, Burton Egbert | That Affair at Elizabeth | 1907 | front matter dated 1907 |
| 29629 | Stevenson, Burton Egbert | The Destroyer: A Tale of International Intrigue | 1913 | front matter dated 1913 |
| 19672 | Stevenson, Burton Egbert | The Holladay case | 1903 | front matter dated 1903 |
| 69112 | Stevenson, Burton Egbert | The quest for the rose of Sharon | 1909 | front matter dated 1909 |
| 42 | Stevenson, Robert Louis | The strange case of Dr. Jekyll and Mr. Hyde |  | all contributors died by 1894 |
| 647 | Stevenson, Robert Louis; Stevenson, Fanny Van de G | The Dynamiter |  | all contributors died by 1914 |
| 1478 | Stewart, Donald Ogden | A Parody Outline of History Wherein May Be Found a Curiously Irreverent Treatment of Ameri | 1916 | front matter dated 1916 |
| 345 | Stoker, Bram | Dracula |  | all contributors died by 1912 |
| 3781 | Stoker, Bram | The Jewel of Seven Stars |  | all contributors died by 1912 |
| 42455 | Stoker, Bram | The Mystery of the Sea |  | all contributors died by 1912 |
| 37434 | Stokes, Katherine | The Motor Maids' School Days | 1911 | front matter dated 1911 |
| 40821 | Stone, A. | Fighting Byng: A Novel of Mystery, Intrigue and Adventure | 1919 | front matter dated 1919 |
| 75577 | Strahan, Kay Cleaver | Footprints | 1929 | front matter dated 1929 |
| 75436 | Strahan, Kay Cleaver | The Desert Moon mystery | 1928 | front matter dated 1928 |
| 41737 | Strang, Herbert | Burton of the Flying Corps | 1916 | front matter dated 1916 |
| 40555 | Strang, Herbert | No Man's Island | 1921 | front matter dated 1921 |
| 30394 | Stratemeyer, Edward | Dave Porter and His Double; Or, The Disapperarance of the Basswood Fortune | 1916 | front matter dated 1916 |
| 24033 | Stratemeyer, Edward | Dave Porter in the Gold Fields; Or, The Search for the Landslide Mine | 1914 | front matter dated 1914 |
| 36377 | Stratemeyer, Edward | Dave Porter on Cave Island; Or, A Schoolboy's Mysterious Mission |  | all contributors died by 1930 |
| 77209 | Stratemeyer, Edward | Larry Barlow's ambition | 1902 | front matter dated 1902 |
| 74197 | Stratemeyer, Edward | Reuben Stone's discovery |  | all contributors died by 1930 |
| 20618 | Stratemeyer, Edward | The Boy Land Boomer; Or, Dick Arbuckle's Adventures in Oklahoma | 1902 | front matter dated 1902 |
| 30864 | Stratemeyer, Edward | The Missing Tin Box; Or, The Stolen Railroad Bonds |  | all contributors died by 1930 |
| 17636 | Stratemeyer, Edward | The Mystery at Putnam Hall: The School Chums' Strange Discovery |  | all contributors died by 1930 |
| 45517 | Stratemeyer, Edward | The Putnam Hall Cadets; or, Good Times in School and Out |  | all contributors died by 1930 |
| 5002 | Stratemeyer, Edward | The Rover Boys in Business; Or, The Search for the Missing Bonds |  | all contributors died by 1930 |
| 5003 | Stratemeyer, Edward | The Rover Boys in New York; Or, Saving Their Father's Honor |  | all contributors died by 1930 |
| 26193 | Stratemeyer, Edward | The Rover Boys in Southern Waters; or, The Deserted Steam Yacht |  | all contributors died by 1930 |
| 20053 | Stratemeyer, Edward | The Rover Boys in the Air; Or, From College Campus to the Clouds |  | all contributors died by 1930 |
| 22996 | Stratemeyer, Edward | The Rover Boys on Snowshoe Island; or, The Old Lumberman's Treasure Box |  | all contributors died by 1930 |
| 22163 | Stratemeyer, Edward | The Rover Boys on the Farm; or, Last Days at Putnam Hall |  | all contributors died by 1930 |
| 69463 | Stratemeyer, Edward | The Rover Boys winning a fortune; or, Strenuous days ashore and afloat | 1926 | front matter dated 1926 |
| 34917 | Streckfuss, Adolf | The Lonely House | 1907 | front matter dated 1907 |
| 18671 | Stringer, Arthur | Never-Fail Blake | 1913 | front matter dated 1913 |
| 19735 | Stringer, Arthur | Phantom Wires: A Novel | 1908 | front matter dated 1908 |
| 33645 | Stringer, Arthur | The Man Who Couldn't Sleep | 1919 | front matter dated 1919 |
| 50203 | Stringer, Arthur | The Wire Tappers | 1906 | front matter dated 1906 |
| 6448 | Sue, Eugène | Mysteries of Paris — Volume 03 |  | all contributors died by 1857 |
| 33800 | Sue, Eugène | The Mysteries of Paris, illustrated with etchings, Vol. 1 |  | all contributors died by 1857 |
| 33804 | Sue, Eugène | The Mysteries of Paris, illustrated with etchings, Vol. 5 |  | all contributors died by 1857 |
| 33805 | Sue, Eugène | The Mysteries of Paris, illustrated with etchings, Vol. 6 |  | all contributors died by 1857 |
| 65559 | Sullivan, Alan | The Jade God | 1925 | front matter dated 1925 |
| 38477 | Sutphen, Van Tassel | In Jeopardy | 1922 | front matter dated 1922 |
| 54333 | Sykes, D. F. E. | Miriam: A Tale of Pole Moor and the Greenfield Hills |  | all contributors died by 1920 |
| 38131 | Taft, William Nelson | On Secret Service Detective-Mystery Stories Based on Real Cases Solved by Government Agent | 1921 | front matter dated 1921 |
| 65345 | Taylor, Bert Leston; Thoits, Alvin T. | Under Three Flags: A Story of Mystery | 1896 | front matter dated 1896 |
| 44881 | Taylor, Meadows | Confessions of a Thug |  | all contributors died by 1876 |
| 67531 | Terhune, Albert Payson | The Amateur Inn | 1923 | front matter dated 1923 |
| 68875 | Thanet, Octave | The lion's share | 1907 | front matter dated 1907 |
| 77033 | Thayer, Lee | The sinister mark | 1923 | front matter dated 1923 |
| 62885 | Theiss, Lewis E. (Lewis Edwin) | The Young Wireless Operator—With the U. S. Secret Service Winning his way in the Secret Se | 1923 | front matter dated 1923 |
| 31135 | Thierry, James Francis | The adventure of the eleven cuff-buttons | 1918 | front matter dated 1918 |
| 20010 | Thompson, Charles Miner | The Calico Cat | 1908 | front matter dated 1908 |
| 27732 | Thompson, George | City Crimes; Or, Life in New York and Boston | 1849 | front matter dated 1849 |
| 70936 | Thorne, Eglanton | The wizard's cave |  | all contributors died by 1907 |
| 40361 | Thorne, Guy | The Air Pirate |  | all contributors died by 1923 |
| 40581 | Thorne, Guy | The Secret Service Submarine: A Story of the Present War |  | all contributors died by 1923 |
| 41829 | Thorne, Guy | The Serf |  | all contributors died by 1923 |
| 37378 | Thorne, Paul; Thorne, Mabel | The Secret Toll | 1922 | front matter dated 1922 |
| 75222 | Thynne, Molly | The Draycott murder mystery | 1928 | front matter dated 1928 |
| 6628 | Townsend, George Alfred | The Life, Crime, and Capture of John Wilkes Booth |  | all contributors died by 1914 |
| 34277 | Tracy, Louis | A Mysterious Disappearance |  | all contributors died by 1928 |
| 76603 | Tracy, Louis | Karl Grier |  | all contributors died by 1928 |
| 58434 | Tracy, Louis | Minkie |  | all contributors died by 1928 |
| 4996 | Tracy, Louis | Number Seventeen |  | all contributors died by 1928 |
| 23150 | Tracy, Louis | The Albert Gate Mystery Being Further Adventures of Reginald Brett, Barrister Detective |  | all contributors died by 1928 |
| 31949 | Tracy, Louis | The Bartlett Mystery |  | all contributors died by 1928 |
| 39432 | Tracy, Louis | The House 'Round the Corner |  | all contributors died by 1928 |
| 40493 | Tracy, Louis | The King of Diamonds: A Tale of Mystery and Adventure |  | all contributors died by 1928 |
| 35691 | Tracy, Louis | The Late Tenant |  | all contributors died by 1928 |
| 47113 | Tracy, Louis | The Message | 1908 | front matter dated 1908 |
| 10110 | Tracy, Louis | The Postmaster's Daughter |  | all contributors died by 1928 |
| 31635 | Tracy, Louis | The Silent Barrier | 1908 | front matter dated 1908 |
| 14853 | Tracy, Louis | The Stowmarket Mystery; Or, A Legacy of Hate |  | all contributors died by 1928 |
| 26447 | Tracy, Louis | The Strange Case of Mortimer Fenley |  | all contributors died by 1928 |
| 50705 | Tracy, Louis | The de Bercy Affair | 1910 | front matter dated 1910 |
| 37545 | Tracy, Virginia | "Persons Unknown" | 1914 | front matter dated 1914 |
| 11987 | Train, Arthur Cheney | By Advice of Counsel | 1921 | front matter dated 1921 |
| 34597 | Train, Arthur Cheney | McAllister and His Double | 1905 | front matter dated 1905 |
| 76689 | Treynor, Albert M. (Albert McKune) | Snow-blind | 1929 | front matter dated 1929 |
| 69773 | Treynor, Albert M. (Albert McKune) | The long patrol | 1924 | front matter dated 1924 |
| 3713 | Trollope, Anthony | Aaron Trow |  | all contributors died by 1882 |
| 5179 | Trollope, Thomas Adolphus | A Siren |  | all contributors died by 1892 |
| 50794 | Tucker, Kate Marion | The Haunted Ship | 1929 | front matter dated 1929 |
| 61996 | Tunney, Thomas J. (Thomas Joseph) | Throttled! The Detection of the German and Anarchist Bomb Plotters | 1919 | front matter dated 1919 |
| 70059 | Tuttle, W. C. (Wilbur C.) | Hidden blood | 1925 | front matter dated 1925 |
| 73207 | Tuttle, W. C. (Wilbur C.) | The Morgan trail | 1928 | front matter dated 1928 |
| 78717 | Tuttle, W. C. (Wilbur C.) | The Silver Bar mystery | 1930 | front matter dated 1930 |
| 3180 | Twain, Mark | A Double Barrelled Detective Story |  | all contributors died by 1910 |
| 3181 | Twain, Mark | The Stolen White Elephant |  | all contributors died by 1910 |
| 102 | Twain, Mark | The Tragedy of Pudd'nhead Wilson |  | all contributors died by 1910 |
| 93 | Twain, Mark | Tom Sawyer, Detective |  | all contributors died by 1910 |
| 77879 | Tyson, J. Aubrey (John Aubrey) | The barge of haunted lives |  | all contributors died by 1930 |
| 75099 | Umbstaetter, H. D. (Herman Daniel); Anderson, Thom | The red-hot dollar, and other stories from the Black Cat | 1911 | front matter dated 1911 |
| 30482 | Upward, Allen | The International Spy Being the Secret History of the Russo-Japanese War |  | all contributors died by 1926 |
| 30910 | Upward, Allen | The Queen Against Owen |  | all contributors died by 1926 |
| 69845 | Upward, Allen | The club of masks |  | all contributors died by 1926 |
| 70788 | Van Dine, S. S. | The "Canary" murder case | 1927 | known first publication: first published 1927 |
| 70634 | Van Dine, S. S. | The Benson murder case | 1926 | known first publication: first published 1926 |
| 75157 | Van Dine, S. S. | The Bishop murder case | 1929 | known first publication: first published 1929 |
| 72719 | Van Dine, S. S. | The Greene murder case | 1928 | known first publication: first published 1928 |
| 78655 | Van Dine, S. S. | The scarab murder case | 1929 | front matter dated 1929 |
| 31021 | Vance, Louis Joseph | The Bandbox | 1912 | front matter dated 1912 |
| 9779 | Vance, Louis Joseph | The Black Bag | 1908 | front matter dated 1908 |
| 32302 | Vance, Louis Joseph | The Destroying Angel | 1912 | front matter dated 1912 |
| 59177 | Vance, Louis Joseph | The Lone Wolf Returns | 1923 | front matter dated 1923 |
| 17303 | Various | Chambers's Edinburgh Journal, No. 429 Volume 17, New Series, March 20, 1852 | 1852 | issue dated 1852 in the title |
| 65598 | Various | Chambers's Journal of Popular Literature, Science, and Art, Fifth Series, No. 19, Vol. I,  | 1884 | issue dated 1884 in the title |
| 47235 | Various | Chambers's Journal of Popular Literature, Science, and Art, No. 699 May 19, 1877 | 1877 | issue dated 1877 in the title |
| 75937 | Various | Chambers's Journal of Popular Literature, Science, and Art, fifth series, no. 153, vol. II | 1886 | issue dated 1886 in the title |
| 19356 | Various | Golden Stories A Selection of the Best Fiction by the Foremost Writers | 1908 | front matter dated 1908 |
| 33046 | Various | Harper's Round Table, July 2, 1895 | 1895 | issue dated 1895 in the title |
| 29454 | Various | Punch or the London Charivari, Vol. 147, November 25, 1914 | 1914 | issue dated 1914 in the title |
| 28382 | Various | Punch or the London Charivari, Vol. 147, October 21, 1914 | 1914 | issue dated 1914 in the title |
| 44933 | Various | Punch or the London Charivari, Vol. 148, February 10, 1915 | 1915 | issue dated 1915 in the title |
| 28360 | Various | Punch, or the London Charivari, Vol. 147, October 14, 1914 | 1914 | issue dated 1914 in the title |
| 27967 | Various | Punch, or the London Charivari, Vol. 147, September 30, 1914 | 1914 | issue dated 1914 in the title |
| 22697 | Various | Punch, or the London Charivari, Vol. 150, February 23, 1916 | 1916 | issue dated 1916 in the title |
| 23064 | Various | Punch, or the London Charivari, Vol. 150, June 7, 1916 | 1916 | issue dated 1916 in the title |
| 14165 | Various | Punch, or the London Charivari, Volume 101, December 12, 1891 | 1891 | issue dated 1891 in the title |
| 14769 | Various | Punch, or the London Charivari, Volume 152, April 11, 1917 | 1917 | issue dated 1917 in the title |
| 14767 | Various | Punch, or the London Charivari, Volume 152, February 21, 1917 | 1917 | issue dated 1917 in the title |
| 14450 | Various | Punch, or the London Charivari, Volume 152, February 7, 1917 | 1917 | issue dated 1917 in the title |
| 14516 | Various | Punch, or the London Charivari, Volume 152, January 31, 1917 | 1917 | issue dated 1917 in the title |
| 11444 | Various | Punch, or the London Charivari, Volume 153, December 12, 1917 | 1917 | issue dated 1917 in the title |
| 11704 | Various | Punch, or the London Charivari, Volume 153, July 25, 1917 | 1917 | issue dated 1917 in the title |
| 19151 | Various | Punch, or the London Charivari, Volume 159, August 11, 1920 | 1920 | issue dated 1920 in the title |
| 10019 | Various | Punchinello, Volume 1, No. 22, August 27, 1870 | 1870 | issue dated 1870 in the title |
| 10017 | Various | Punchinello, Volume 1, No. 23, September 3, 1870 | 1870 | issue dated 1870 in the title |
| 10034 | Various | Punchinello, Volume 1, No. 26, September 24, 1870 | 1870 | issue dated 1870 in the title |
| 10047 | Various | Punchinello, Volume 2, No. 29, October 15, 1870 | 1870 | issue dated 1870 in the title |
| 68160 | Various | The black cat, vol. I, no. 3, December 1895 | 1895 | front matter dated 1895 |
| 68957 | Various | Weird Tales, Volume 1, Number 1, March 1923: The unique magazine | 1923 | front matter dated 1923 |
| 69606 | Various | Weird Tales, Volume 1, Number 2, April, 1923: The unique magazine | 1923 | front matter dated 1923 |
| 69607 | Various | Weird Tales, Volume 1, Number 3, May, 1923: The unique magazine | 1923 | front matter dated 1923 |
| 69608 | Various | Weird Tales, Volume 1, Number 4, June, 1923: The unique magazine | 1923 | front matter dated 1923 |
| 23489 | Verne, Jules | Godfrey Morgan: A Californian Mystery |  | all contributors died by 1905 |
| 39576 | Verrill, A. Hyatt (Alpheus Hyatt) | The Radio Detectives | 1922 | front matter dated 1922 |
| 42569 | Verrill, A. Hyatt (Alpheus Hyatt) | The Radio Detectives Under the Sea | 1922 | front matter dated 1922 |
| 42545 | Verrill, A. Hyatt (Alpheus Hyatt) | The Radio Detectives in the Jungle | 1922 | front matter dated 1922 |
| 54888 | Vesey, A. H. (Arthur Henry) | The Clock and the Key | 1905 | front matter dated 1905 |
| 46708 | Victor, Metta Victoria Fuller | The Dead Letter: An American Romance |  | all contributors died by 1885 |
| 75318 | Wade, Henry | The Duke of York's steps | 1929 | front matter dated 1929 |
| 52180 | Walcott, Earle Ashley | The Apple of Discord | 1907 | front matter dated 1907 |
| 22212 | Walk, Charles Edmonds | The Paternoster Ruby | 1910 | front matter dated 1910 |
| 69106 | Walk, Charles Edmonds | The silver blade: The true chronicle of a double mystery | 1908 | front matter dated 1908 |
| 72316 | Wallace, Edgar | Angel Esquire | 1927 | front matter dated 1927 |
| 74687 | Wallace, Edgar | Captains of souls | 1922 | front matter dated 1922 |
| 65383 | Wallace, Edgar | Diana of Kara-Kara | 1924 | front matter dated 1924 |
| 78794 | Wallace, Edgar | Gunman's bluff | 1928 | front matter dated 1928 |
| 76212 | Wallace, Edgar | Kate plus 10 | 1917 | front matter dated 1917 |
| 76168 | Wallace, Edgar | Room 13 | 1924 | front matter dated 1924 |
| 21530 | Wallace, Edgar | The Angel of Terror | 1922 | front matter dated 1922 |
| 75643 | Wallace, Edgar | The Black Abbot | 1926 | front matter dated 1926 |
| 24933 | Wallace, Edgar | The Man Who Knew | 1918 | front matter dated 1918 |
| 64907 | Wallace, Edgar | The Other Man | 1911 | front matter dated 1911 |
| 26176 | Wallace, Edgar | The Secret House | 1919 | front matter dated 1919 |
| 69788 | Wallace, Edgar | The avenger | 1926 | front matter dated 1926 |
| 70882 | Wallace, Edgar | The clue of the new pin | 1923 | front matter dated 1923 |
| 79658 | Wallace, Edgar | The fourth plague | 1930 | front matter dated 1930 |
| 76677 | Wallace, Edgar | The girl from Scotland Yard | 1926 | front matter dated 1926 |
| 78508 | Wallace, Edgar | The hand of power | 1930 | front matter dated 1930 |
| 75858 | Wallace, Edgar | The strange countess | 1926 | front matter dated 1926 |
| 77976 | Wallace, Edgar | The valley of ghosts | 1923 | front matter dated 1923 |
| 21228 | Walton, Amy | White Lilac; or the Queen of the May |  | all contributors died by 1899 |
| 50287 | Walton, Frank | The Flying Machine Boys in the Wilds; Or, The Mystery of the Andes | 1913 | front matter dated 1913 |
| 50165 | Walton, Frank | The Flying Machine Boys on Duty; Or, The Clue Above the Clouds | 1913 | front matter dated 1913 |
| 50824 | Walton, Frank | The Flying Machine Boys on Secret Service; Or, The Capture in the Air | 1913 | front matter dated 1913 |
| 33662 | Ward, Herbert D. (Herbert Dickinson) | A Republic Without a President, and Other Stories | 1891 | front matter dated 1891 |
| 14174 | Ward, Humphry, Mrs. | The Mating of Lydia |  | all contributors died by 1920 |
| 79772 | Ward, William (Author at Arthur Westbrook Co. (Cle | Jeff Clayton's surprise | 1910 | front matter dated 1910 |
| 72314 | Warden, Florence | A lady in black |  | all contributors died by 1929 |
| 73798 | Warden, Florence | Mystery of the inn by the shore |  | all contributors died by 1929 |
| 72089 | Warden, Florence | Sea Mew Abbey |  | all contributors died by 1929 |
| 68544 | Warden, Florence | St. Cuthbert's tower |  | all contributors died by 1929 |
| 71788 | Warden, Florence | The house on the marsh |  | all contributors died by 1929 |
| 72669 | Warden, Florence | The mis-rule of three |  | all contributors died by 1929 |
| 71864 | Warden, Florence | The white countess |  | all contributors died by 1929 |
| 20985 | Warren, George A. | The Banner Boy Scouts on a Tour; or, The Mystery of Rattlesnake Mountain | 1912 | front matter dated 1912 |
| 12371 | Warren, Samuel | The Experiences of a Barrister, and Confessions of an Attorney |  | all contributors died by 1877 |
| 53133 | Watson, H. B. Marriott (Henry Brereton Marriott) | The High Toby Being further chapters in the life and fortunes of Dick Ryder, otherwise Gal |  | all contributors died by 1921 |
| 45658 | Watson, John R. (John Reay); Rees, Arthur J. (Arth | The Mystery of the Downs | 1918 | front matter dated 1918 |
| 54916 | Wayne, Charles Stokes | A Prince to Order |  | all contributors died by 1920 |
| 47471 | Webb, Marion St. John | The Girls of Chequertrees | 1923 | front matter dated 1923 |
| 69511 | Webster, Frank V. | Ben Hardy's flying machine; or, Making a record for himself | 1911 | front matter dated 1911 |
| 21842 | Webster, Frank V. | The Boy Scouts of Lenox; Or, The Hike Over Big Bear Mountain | 1915 | front matter dated 1915 |
| 21794 | Webster, Frank V. | The Boy from the Ranch; Or, Roy Bradner's City Experiences | 1909 | front matter dated 1909 |
| 68471 | Webster, Frank V. | Tom the telephone boy; or, The mystery of a message | 1909 | front matter dated 1909 |
| 76546 | Webster, Henry Kitchell | The Corbin necklace | 1926 | front matter dated 1926 |
| 21264 | Webster, Jean | The Four-Pools Mystery |  | all contributors died by 1923 |
| 59772 | Weekes, R. K. (Rose Kirkpatrick) | Convict B 14: A Novel | 1920 | front matter dated 1920 |
| 60185 | Weigall, Arthur E. P. Brome (Arthur Edward Pearse  | Bedouin Love | 1922 | front matter dated 1922 |
| 43351 | Wells, Carolyn | A Chain of Evidence | 1912 | front matter dated 1912 |
| 59126 | Wells, Carolyn | Faulkner's Folly | 1917 | front matter dated 1917 |
| 75642 | Wells, Carolyn | Feathers left around | 1923 | front matter dated 1923 |
| 35254 | Wells, Carolyn | In the Onyx Lobby | 1920 | front matter dated 1920 |
| 25847 | Wells, Carolyn | Patty's Friends | 1908 | front matter dated 1908 |
| 77966 | Wells, Carolyn | Spooky Hollow | 1923 | front matter dated 1923 |
| 54869 | Wells, Carolyn | The Clue | 1909 | front matter dated 1909 |
| 30868 | Wells, Carolyn | The Come Back | 1921 | front matter dated 1921 |
| 45622 | Wells, Carolyn | The Curved Blades | 1916 | front matter dated 1916 |
| 46064 | Wells, Carolyn | The Deep Lake Mystery | 1928 | front matter dated 1928 |
| 35022 | Wells, Carolyn | The Diamond Pin | 1919 | front matter dated 1919 |
| 42714 | Wells, Carolyn | The Luminous Face | 1921 | front matter dated 1921 |
| 44872 | Wells, Carolyn | The Man Who Fell Through the Earth | 1919 | front matter dated 1919 |
| 44841 | Wells, Carolyn | The Mark of Cain | 1917 | front matter dated 1917 |
| 44984 | Wells, Carolyn | The Mystery Girl | 1922 | front matter dated 1922 |
| 50209 | Wells, Carolyn | The Mystery of the Sycamore | 1921 | front matter dated 1921 |
| 46008 | Wells, Carolyn | The Room with the Tassels | 1918 | front matter dated 1918 |
| 45912 | Wells, Carolyn | The Vanishing of Betty Varian | 1922 | front matter dated 1922 |
| 62963 | Wentworth, Patricia | The Astonishing Adventure of Jane Smith | 1923 | front matter dated 1923 |
| 62820 | Wentworth, Patricia | The Fire Within | 1913 | front matter dated 1913 |
| 24350 | Wharton, Edith | Kerfol 1916 | 1916 | front matter dated 1916 |
| 37149 | Wheeler, Edward L. (Edward Lytton) | Fritz to the Front, or, the Ventriloquist Scamp-Hunter |  | all contributors died by 1885 |
| 40586 | Wheeler, Janet D. | Billie Bradley and Her Classmates; Or, The Secret of the Locked Tower | 1921 | front matter dated 1921 |
| 50157 | Wheeler, Janet D. | Billie Bradley and the School Mystery; Or, The Girl From Oklahoma | 1930 | front matter dated 1930 |
| 25762 | Wheeler, Janet D. | Billie Bradley on Lighthouse Island; Or, The Mystery of the Wreck | 1920 | front matter dated 1920 |
| 50723 | Wheeler, R. L. | The Demon Cruiser | 1909 | front matter dated 1909 |
| 1632 | Whibley, Charles | A Book of Scoundrels |  | all contributors died by 1930 |
| 25753 | Whipple, Wayne; Aaron, S. F. (Samuel Francis) | Radio Boys Loyalty; Or, Bill Brown Listens In | 1922 | front matter dated 1922 |
| 36198 | Whitaker, Herman | The Mystery of The Barranca |  | all contributors died by 1919 |
| 57066 | White, Fred M. (Fred Merrick) | The Corner House | 1906 | front matter dated 1906 |
| 43492 | White, Fred M. (Fred Merrick) | The Five Knots | 1908 | front matter dated 1908 |
| 56960 | White, Fred M. (Fred Merrick) | The Midnight Guest: A Detective Story | 1907 | front matter dated 1907 |
| 48882 | White, Fred M. (Fred Merrick) | The Mystery of the Ravenspurs A Romance and Detective Story of Thibet and England | 1911 | front matter dated 1911 |
| 27395 | White, Fred M. (Fred Merrick) | The Slave of Silence | 1906 | front matter dated 1906 |
| 55006 | White, Fred M. (Fred Merrick) | The Sundial | 1908 | front matter dated 1908 |
| 57314 | White, Fred M. (Fred Merrick) | The Yellow Face | 1907 | front matter dated 1907 |
| 57760 | White, George M. (George Miles) | From Boniface to Bank Burglar; Or, The Price of Persecution How a Successful Business Man, | 1905 | front matter dated 1905 |
| 57302 | White, Ida Belle | Spirits do return | 1915 | front matter dated 1915 |
| 34567 | White, William Patterson | Paradise Bend | 1920 | front matter dated 1920 |
| 68752 | Whitehead, Charles | Lives and exploits of the most noted highwaymen, robbers and murderers of all nations Draw |  | all contributors died by 1862 |
| 40398 | Whitlock, Brand | The Turn of the Balance | 1907 | front matter dated 1907 |
| 11085 | Whyte-Melville, G. J. (George John) | M. or N. "Similia similibus curantur." |  | all contributors died by 1878 |
| 42333 | Wilkins, W. A. | The Cleverdale Mystery; or, The Machine and Its Wheels: A Story of American Life | 1882 | front matter dated 1882 |
| 76059 | Williams, Harper | The thing in the woods | 1924 | front matter dated 1924 |
| 65416 | Williams, Valentine | Clubfoot the Avenger Being some further adventures of Desmond Oakwood, of the Secret Servi | 1923 | front matter dated 1923 |
| 32428 | Williamson, A. M. (Alice Muriel); Williamson, C. N | The Brightener | 1921 | front matter dated 1921 |
| 38470 | Williamson, C. N. (Charles Norris); Williamson, A. | Lord John in New York | 1918 | front matter dated 1918 |
| 56470 | Williamson, C. N. (Charles Norris); Williamson, A. | The Great Pearl Secret | 1921 | front matter dated 1921 |
| 21998 | Williamson, C. N. (Charles Norris); Williamson, A. | The Lion's Mouse | 1919 | front matter dated 1919 |
| 42167 | Wills, C. J. (Charles James) | The Pit Town Coronet: A Family Mystery, Volume 1 (of 3) |  | all contributors died by 1912 |
| 42168 | Wills, C. J. (Charles James) | The Pit Town Coronet: A Family Mystery, Volume 2 (of 3) |  | all contributors died by 1912 |
| 42169 | Wills, C. J. (Charles James) | The Pit Town Coronet: A Family Mystery, Volume 3 (of 3) |  | all contributors died by 1912 |
| 65172 | Wodehouse, P. G. (Pelham Grenville) | A Gentleman of Leisure | 1921 | front matter dated 1921 |
| 72972 | Wodehouse, P. G. (Pelham Grenville) | Money for nothing | 1928 | front matter dated 1928 |
| 58288 | Wood, Henry, Mrs. | Bessy Rane: A Novel |  | all contributors died by 1887 |
| 40928 | Wood, Henry, Mrs. | Johnny Ludlow, Second Series |  | all contributors died by 1887 |
| 40963 | Wood, Henry, Mrs. | Johnny Ludlow, Sixth Series |  | all contributors died by 1887 |
| 58086 | Wood, Henry, Mrs. | Roland Yorke A Sequel to "The Channings" |  | all contributors died by 1887 |
| 59144 | Wood, Henry, Mrs. | The Master of Greylands: A Novel |  | all contributors died by 1887 |
| 38624 | Wood, Henry, Mrs. | The Story of Charles Strange: A Novel. Vol. 2 (of 3) |  | all contributors died by 1887 |
| 38625 | Wood, Henry, Mrs. | The Story of Charles Strange: A Novel. Vol. 3 (of 3) |  | all contributors died by 1887 |
| 58346 | Wood, Henry, Mrs. | Within the Maze: A Novel, Vol. 2 (of 2) |  | all contributors died by 1887 |
| 25820 | Woodrow, Wilson, Mrs. | The Silver Butterfly | 1908 | front matter dated 1908 |
| 47445 | Wooldridge, Clifton R. (Clifton Rodman) | Twenty Years a Detective in the Wickedest City in the World | 1908 | front matter dated 1908 |
| 32707 | Woolson, Constance Fenimore | Anne: A Novel |  | all contributors died by 1896 |
| 28780 | Worts, George F. (George Frank) | Peter the Brazen: A Mystery Story of Modern China | 1919 | front matter dated 1919 |
| 59060 | Wright, Rowland | The Disappearance of Kimball Webb | 1919 | front matter dated 1919 |
| 57230 | Wyman, L. P. (Levi Parker) | The Golden Boys Along the River Allagash | 1923 | front matter dated 1923 |
| 58595 | Wyman, L. P. (Levi Parker) | The Golden Boys Rescued by Radio | 1923 | front matter dated 1923 |
| 62802 | Wyman, L. P. (Levi Parker) | The Golden Boys at the Haunted Camp | 1924 | front matter dated 1924 |
| 76521 | Wyman, L. P. (Levi Parker) | The Hunniwell boys and the platinum mystery | 1928 | front matter dated 1928 |
| 59366 | Yates, Edmund | Running the Gauntlet: A Novel |  | all contributors died by 1894 |
| 62298 | Yates, Edmund | The Impending Sword: A Novel (Vol. 3 of 3) |  | all contributors died by 1894 |
| 3744 | Yonge, Charlotte M. (Charlotte Mary) | The Trial; Or, More Links of the Daisy Chain |  | all contributors died by 1901 |
| 44788 | Young, Clarence | The Motor Boys Afloat; or, The Stirring Cruise of the Dartaway | 1908 | front matter dated 1908 |
| 53704 | Young, Clarence | The Motor Boys Bound for Home; or, Ned, Bob and Jerry on the Wrecked Troopship | 1920 | front matter dated 1920 |
| 45576 | Young, Clarence | The Motor Boys Over the Rockies; Or, A Mystery of the Air | 1911 | front matter dated 1911 |
| 75395 | Young, Clarence | The Racer boys on the prairies | 1913 | front matter dated 1913 |
| 28164 | Zangwill, Israel | The Big Bow Mystery |  | all contributors died by 1926 |
| 63791 | Zola, Émile | For a Night of Love |  | all contributors died by 1902 |
| 6626 | Zola, Émile | Theresa Raquin |  | all contributors died by 1922 |
| 55849 | Zola, Émile | Truth [Vérité] |  | all contributors died by 1922 |

## noir (58 books)

| Gutenberg ID | Author | Title | Year | PD basis |
|---|---|---|---|---|
| 79392 | Burnett, W. R. (William Riley) | Little Caesar | 1929 | known first publication: first published 1929 |
| 62428 | Carter, Nicholas (House name) | A Battle for Right; Or, A Clash of Wits | 1916 | front matter dated 1916 |
| 63143 | Carter, Nicholas (House name) | A Broken Bond; Or, The Man Without Morals | 1917 | front matter dated 1917 |
| 64147 | Carter, Nicholas (House name) | A Stolen Name; Or, The Man Who Defied Nick Carter | 1910 | front matter dated 1910 |
| 26704 | Carter, Nicholas (House name) | A Woman at Bay; Or, A Fiend in Skirts | 1907 | front matter dated 1907 |
| 61514 | Carter, Nicholas (House name) | Captain Sparkle, Pirate; Or, A Hard Man to Catch | 1905 | front matter dated 1905 |
| 62860 | Carter, Nicholas (House name) | Hidden Foes; Or, A Fatal Miscalculation | 1917 | front matter dated 1917 |
| 73636 | Carter, Nicholas (House name) | New Nick Carter weekly, No. 11, March 13, 1897: Trim in the wilds; or, hunting a criminal  | 1897 | issue dated 1897 in the title |
| 69108 | Carter, Nicholas (House name) | New Nick Carter weekly; No. 28. July 10, 1897; Nick Carter at the track; or, How he became | 1897 | issue dated 1897 in the title |
| 66486 | Carter, Nicholas (House name) | Nick Carter Stories No. 135. April 10, 1915; Straight to the Goal; Or, Nick Carter's Queer | 1915 | issue dated 1915 in the title |
| 66542 | Carter, Nicholas (House name) | Nick Carter Stories No. 138 May 1, 1915; The Traitors of the Tropics; or, Nick Carter's Ro | 1915 | issue dated 1915 in the title |
| 69032 | Carter, Nicholas (House name) | Nick Carter weekly No. 186, July 21, 1900: Nick Carter rescues a daughter; or, The junior  | 1900 | issue dated 1900 in the title |
| 61135 | Carter, Nicholas (House name) | Out of Death's Shadow; Or, A Case Without a Precedent | 1905 | front matter dated 1905 |
| 66724 | Carter, Nicholas (House name) | The Four-Fingered Glove; Or, The Cost of a Lie | 1904 | front matter dated 1904 |
| 63340 | Carter, Nicholas (House name) | The Great Diamond Syndicate; Or, The Hardest Crew on Record | 1909 | front matter dated 1909 |
| 63864 | Carter, Nicholas (House name) | The Man Without a Conscience; Or, From Rogue to Convict | 1906 | front matter dated 1906 |
| 66740 | Carter, Nicholas (House name) | The Stolen Brain; Or, A Wonderful Crime | 1914 | front matter dated 1914 |
| 65783 | Carter, Nicholas (House name) | The Twin Mystery; Or, A Dashing Rescue | 1903 | front matter dated 1903 |
| 68697 | Carter, Nicholas (House name) | Toying with fate; or, Nick Carter's narrow shave | 1903 | front matter dated 1903 |
| 65790 | Carter, Nicholas (House name) | Under the Tiger's Claws; Or, A Struggle for the Right | 1905 | front matter dated 1905 |
| 67615 | Carter, Nicholas (House name); Boston, Ralph | Nick Carter Stories No. 148, July 10, 1915; The Mark of Cain; or, Nick Carter's Air-line C | 1915 | issue dated 1915 in the title |
| 68094 | Carter, Nicholas (House name); Boston, Ralph | Nick Carter Stories No. 149, July 17, 1915: A Network of Crime; or, Nick Carter's Tangled  | 1915 | issue dated 1915 in the title |
| 68116 | Carter, Nicholas (House name); Boston, Ralph | Nick Carter Stories No. 150, July 24, 1915: The House of Fear; or, Nick Carter's Counterst | 1915 | issue dated 1915 in the title |
| 68089 | Carter, Nicholas (House name); Boston, Ralph | Nick Carter Stories No. 151, July 31, 1915: The Mystery of the Crossed Needles; or Nick Ca | 1915 | issue dated 1915 in the title |
| 68106 | Carter, Nicholas (House name); Boston, Ralph | Nick Carter Stories No. 152, August 7, 1915: The Forced Crime; or, Nick Carter's Brazen Cl | 1915 | issue dated 1915 in the title |
| 67617 | Carter, Nicholas (House name); Boston, Ralph; Clar | Nick Carter Stories No. 147, July 3, 1915: On Death's Trail; or, Nick Carter's Strangest C | 1915 | issue dated 1915 in the title |
| 67082 | Carter, Nicholas (House name); Bradshaw, Alden F. | Nick Carter Stories No. 11, November 23, 1912: Nick Carter Strikes Oil; or, Uncovering Mor | 1912 | issue dated 1912 in the title |
| 68376 | Carter, Nicholas (House name); Jenkins, Burke | Nick Carter Stories No. 120, December 26, 1914: An uncanny revenge; or, Nick Carter and th | 1914 | issue dated 1914 in the title |
| 68460 | Carter, Nicholas (House name); Jenkins, Burke | Nick Carter Stories No. 121, January 2, 1915: The call of death; or, Nick Carter's clever  | 1915 | issue dated 1915 in the title |
| 69385 | Carter, Nicholas (House name); Jenkins, Burke | Nick Carter Stories No. 124, January 23, 1915: The girl kidnaper; or, Nick Carter's up-to- | 1915 | issue dated 1915 in the title |
| 68467 | Carter, Nicholas (House name); Jenkins, Burke; Nos | Nick Carter Stories No. 122, January 9, 1915: The suicide; or, Nick Carter and the lost he | 1915 | issue dated 1915 in the title |
| 68140 | Carter, Nicholas (House name); Lebhar, Bertram | Nick Carter Stories No. 154, August 21, 1915: The mask of death; or, Nick Carter's curious | 1915 | issue dated 1915 in the title |
| 68108 | Carter, Nicholas (House name); Lebhar, Bertram | Nick Carter Stories No. 155, August 28, 1915: The Gordon Elopement; or, Nick Carter's Thre | 1915 | issue dated 1915 in the title |
| 68474 | Carter, Nicholas (House name); Lebhar, Bertram | Nick Carter Stories No. 157, September 11, 1915: A human counterfeit; or, Nick Carter and  | 1915 | issue dated 1915 in the title |
| 68360 | Carter, Nicholas (House name); Lebhar, Bertram | Nick Carter Stories No. 158, September 18, 1915: The blue veil; or, Nick Carter's torn tra | 1915 | issue dated 1915 in the title |
| 68338 | Carter, Nicholas (House name); Lebhar, Bertram; St | Nick Carter Stories No. 160, October 2, 1915: The Yellow Label; or, Nick Carter and the So | 1915 | issue dated 1915 in the title |
| 65805 | Carter, Nicholas (House name); Phillips, Roland As | Nick Carter Stories No. 131, March 13, 1915: A fatal message; or, Nick Carter's slender cl | 1915 | issue dated 1915 in the title |
| 66738 | Carter, Nicholas (House name); Phillips, Roland As | Nick Carter Stories No. 133, March 27, 1915: Won by Magic; or, Nick Carter's Mysterious Ea | 1915 | issue dated 1915 in the title |
| 66750 | Carter, Nicholas (House name); Phillips, Roland As | Nick Carter Stories No. 136, April 17, 1915: The Man They Held Back | 1915 | issue dated 1915 in the title |
| 66986 | Carter, Nicholas (House name); Phillips, Roland As | Nick Carter Stories No. 137, April 24, 1915: The Seal of Gijon; Or, Nick Carter's Ice-Hous | 1915 | issue dated 1915 in the title |
| 66758 | Carter, Nicholas (House name); Phillips, Roland As | Nick Carter Stories No. 139, May 8, 1915: The Pressing Peril | 1915 | issue dated 1915 in the title |
| 66764 | Carter, Nicholas (House name); Waddell, C. C. (Cha | Nick Carter Stories No. 140, May 15, 1915: The Melting-Pot | 1915 | issue dated 1915 in the title |
| 66782 | Carter, Nicholas (House name); Waddell, C. C. (Cha | Nick Carter Stories No. 141, May 22, 1915: The duplicate night | 1915 | issue dated 1915 in the title |
| 68499 | Carter, Nicholas (House name); Waddell, C. C. (Cha | Nick Carter Stories No. 143, June 5, 1915: The sultan's pearls; or, Nick Carter's Porto Ri | 1915 | issue dated 1915 in the title |
| 68022 | Carter, Nicholas (House name); Waddell, C. C. (Cha | Nick Carter Stories No. 145, June 19, 1915: An Unsolved Mystery; Or, Nick Carter's Governm | 1915 | issue dated 1915 in the title |
| 67618 | Carter, Nicholas (House name); Waddell, C. C. (Cha | Nick Carter Stories No. 146, June 26, 1915: Paying the Price; or, Nick Carter's Perilous V | 1915 | issue dated 1915 in the title |
| 77600 | Hammett, Dashiell | The Maltese falcon | 1930 | known first publication: first published in book form 1930 |
| 35818 | Packard, Frank L. (Frank Lucius) | Doors of the Night | 1922 | known first publication: first published 1922 |
| 51939 | Packard, Frank L. (Frank Lucius) | From Now On | 1919 | known first publication: first published 1919 |
| 51965 | Packard, Frank L. (Frank Lucius) | Pawned | 1921 | known first publication: first published 1921 |
| 1218 | Packard, Frank L. (Frank Lucius) | The Adventures of Jimmie Dale | 1917 | known first publication: first published 1917 |
| 59895 | Packard, Frank L. (Frank Lucius) | The Four Stragglers | 1923 | known first publication: first published 1923 |
| 9440 | Packard, Frank L. (Frank Lucius) | The Further Adventures of Jimmie Dale | 1917 | known first publication: first published 1917 |
| 15578 | Packard, Frank L. (Frank Lucius) | The Miracle Man | 1914 | known first publication: first published 1914 |
| 33634 | Packard, Frank L. (Frank Lucius) | The Night Operator | 1919 | known first publication: first published 1919 |
| 51983 | Packard, Frank L. (Frank Lucius) | The Sin That Was His | 1917 | known first publication: first published 1917 |
| 1741 | Packard, Frank L. (Frank Lucius) | The White Moll | 1920 | known first publication: first published 1920 |
| 52084 | Packard, Frank L. (Frank Lucius) | The Wire Devils | 1918 | known first publication: first published 1918 |
