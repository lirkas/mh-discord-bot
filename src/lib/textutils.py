import logging as log
import datetime

from PIL import Image
from PIL import Image, ImageFont, ImageDraw

# set it to false if encoding errors arise while printing text tables 
extended_ascii_support = True

default_font = None
default_image_path = None


class TableSegments:
    'Defines which characters are used for specific segments of the table'

    def __init__(self, top_left, top_mid, top_right, 
                 left, mid, right, 
                 bot_left, bot_mid, bot_right,
                 horiz, vert):
                 
        self.top_left = top_left
        self.top_mid = top_mid
        self.top_right = top_right
        self.left = left
        self.mid = mid
        self.right = right
        self.bot_left = bot_left
        self.bot_mid = bot_mid
        self.bot_right = bot_right
        self.horiz = horiz
        self.vert = vert

class Color:
    '''
    Defines a color using ANSI escape sequences.\n
    Mostly used for terminals.
    '''
    def __init__(self, name: str, code: int):
        self.name = name
        self.code = code
        self.code_start = '\033['+str(code)+'m'
        self.code_end = '\033[0m'
        
    def text(self, text: str) -> str:
        '''
        Wraps the text to have that object's color.
        '''
        return self.code_start + text.replace('\b', '') + self.code_end

# the default charset 
# best compatibility
default_tbl_d = TableSegments (
    '+', '+', '+', 
    '+', '+', '+', 
    '+', '+', '+',
    '-', '|'
)

# extra charset using extended ascii characters (cp437)
# less compatible
slim_tbl_d = TableSegments (
    u'\u250c',u'\u252C',u'\u2510',
    u'\u251C',u'\u253C',u'\u2524',
    u'\u2514',u'\u2534',u'\u2518',
    u'\u2500',u'\u2502'
)
thick_tbl_d = TableSegments (
    u'\u2554',u'\u2566',u'\u2557',
    u'\u2560',u'\u256C',u'\u2563',
    u'\u255a',u'\u2569',u'\u255d',
    u'\u2550',u'\u2551'
)

# Basic color definitions
grey = Color('white', 30)
red = Color('red', 31)
green = Color('green', 32)
yellow = Color('yellow', 33)
blue = Color('blue', 34)
purple = Color('purple', 35)
cyan = Color('cyan', 36)
white = Color('white', 37)


def text_table(content: list[list], row_height = 1, min_column_size = 0, column_sizes: list[int] = None,
               padding: int = 0,
               table_delimiters: TableSegments = default_tbl_d):
    '''
    Creates an ASCII-style text table and populates it with content\n
    `content`           : 2D matrix that hold each cell's value\n
    `row_height`        : !! NOT FULLY WORKING !!\n
    `min_column_size`   : minimum width each column shoud have\n
    `column_sizes`      : array of int that defines each column max width\n
    `padding`           : left and right padding for columns\n
    `table_delimiters`  : TableSegments object containing characters used to write the table\n
    '''
    
    log.info('creating text table')
    # positions for content's cells
    r = 0
    c = 0

    tbl_d = table_delimiters
    # if the encoding is not supported - use default
    if not extended_ascii_support:
        tbl_d = default_tbl_d

    table_text = ''
    cell_text = ''

    row_blocks = len(content)
    column_blocks = len(content[0])
    log.debug('table_size: '+str(row_blocks)+'x'+str(column_blocks)+' blocks')

    # exact amount of 'characters rows'
    rows = (row_blocks * (1 + row_height)) + 1 

    # update column sizes based on padding
    for c in range(0,len(column_sizes)):
        # only for text
        if content[0][c].strip() != '':
            column_sizes[c] += padding*2

    # automatically verify the max width for each column
    # based on each cell content
    # adds paddings if required
    if column_sizes == None:
        log.info('verifying columns sizes')
        column_sizes = [min_column_size] * column_blocks

    while r < row_blocks:
        c = 0
        while c < column_blocks:
            # stringify content
            content[r][c] = str(content[r][c])
            # only pad text
            if content[r][c].strip() != '':
                text_size = len(content[r][c])
                content[r][c] = '{: ^{padding}}'.format(
                     content[r][c], padding=text_size + padding*2)
            content_size = len(content[r][c])
            #             5 > 4 +2    
            if content_size > column_sizes[c]:
                log.debug(str(column_sizes[c]) +'<'+ str(content_size))
                column_sizes[c] = content_size
            c += 1
        r += 1
    log.info('columns sizes have been defined')
    log.debug('  column_sizes = '+str(column_sizes))

    columns = 0
    for size in column_sizes:
        columns += size
    # exact amount of 'characters rows'
    columns = columns + column_blocks + 1

    log.info('table size: ' + str(rows) + 'x' + str(columns) +
        ' (' +str(rows * columns) + ')')

    is_content_row = False
    is_separator_row = False
    is_text_added = False
    r = 0
    c = 0
    row = 0
    row_block = -1
    column = 0
    column_block = 0

    while row < rows:

        log.debug('row START')
        log.debug('current row: ' + str(row))

        # any row
        tbl_d_left = tbl_d.left
        tbl_d_mid = tbl_d.mid
        tbl_d_right = tbl_d.right

        # top row
        if row == 0:
            
            tbl_d_left = tbl_d.top_left
            tbl_d_mid = tbl_d.top_mid
            tbl_d_right = tbl_d.top_right

        # bottom row
        if row == rows -1:
            tbl_d_left = tbl_d.bot_left
            tbl_d_mid = tbl_d.bot_mid
            tbl_d_right = tbl_d.bot_right

        # check what kind of row we are on
        row_type = (row - row_height) % (row_height + 1)
        is_content_row = True if row_type == 0 else False
        is_separator_row = True if row_type == 1 else False

        if is_separator_row:
            row_block += 1
            r = row_block

        log.debug('row type=' + str(row_type))
        
        line = ''
        c = 0
        column = 0
        column_block = 0
        while column_block < column_blocks:
            log.debug('column START')
            log.debug('[block_pos] '+'row:'+str(row_block)+' col:'+str(column_block))
            log.debug('[char_pos] '+'row:'+str(row)+' col:'+str(column))

            # any column block
            col_d_left = tbl_d_mid
            col_d_right = tbl_d_mid

            # left-most column block
            if column_block == 0:
                col_d_left = tbl_d_left
                col_d_right = tbl_d_mid
            
            # right-most column block
            if column_block == column_blocks - 1:
                col_d_left = tbl_d_mid
                col_d_right = tbl_d_right

            # checking which kind of row we are on
            if is_separator_row:
                    col_d_mid = tbl_d.horiz
            elif is_content_row:
                    cell_text = content[r][c]
                    col_d_mid = ' '
                    col_d_left = tbl_d.vert
                    col_d_right = tbl_d.vert
            elif not is_content_row and not is_separator_row:
                    col_d_mid = ' '
                    col_d_left = tbl_d.vert
                    col_d_right = tbl_d.vert

            c_pos = 0
            column_block_width = column_sizes[column_block]

            # iterate for each column inside a column block
            while c_pos <= column_block_width:
                
                # first column in that block
                if c_pos == 0:
                    line += col_d_left
                    log.debug('column_block START')
                # add the text into that cell
                elif is_content_row and not is_text_added:
                        
                        line += str(cell_text)
                        c_pos += len(str(cell_text)) - 1
                        column += c_pos
                        is_text_added = True
                        log.debug('text added to the cell: '+str(cell_text))
                else:
                    line += col_d_mid

                c_pos += 1
                column += 1

            log.debug('column_block END')
            # if its the last column block - close it
            if column_block == column_blocks - 1:
                line += col_d_right
                log.debug('column END')

            column_block += 1
            c += 1
            is_text_added = False
        table_text += line + '\n'
        log.debug('new line added\n'+line)
        row += 1
        log.debug('row END')

    log.info('text table created')
    return table_text

def text_to_image(text, image_path: str, font_path: str, 
                  font_size: int = 30, padding: int = 30, 
                  format: str = 'png',
                  text_rgb: tuple[int,int,int] = (255, 255, 255), 
                  background_rgb: tuple[int,int,int] = (0, 0, 0)):
    ''' 
    Converts text into png image.
    White text on grey backgound\n

        `text_rbg` and `background_rgb` color values order is (red, green, blue)\n
        `format`: valid values: png, bmp, jpeg\n
        `font_size`: font size in pixels\n
        `padding`: left and right padding in pixels, for the whole image\n
    '''


    # Loading Font
    fnt: ImageFont.FreeTypeFont = ImageFont.truetype(font_path, font_size)

    # Determining text size in pixels
    dummy_img = Image.new('RGB', (0, 0), color = (0,0,0,0))
    dummy_imgdraw = ImageDraw.Draw(dummy_img, 'RGB')
    text_bb = dummy_imgdraw.multiline_textbbox((0, 0), text, font=fnt)

    text_h = text_bb[3]
    text_w = text_bb[2]

    img_h = text_h + padding*2
    img_w = text_w + padding*2

    # Generating Image
    img = Image.new('RGB', (img_w, img_h), color=background_rgb+(255,))
    imgdraw = ImageDraw.Draw(img, 'RGB')
    imgdraw.text((padding, padding), text, font=fnt, fill=text_rgb+(255,))
    img.save(image_path, format=format)

def test_ascii_support() -> bool:
    '''
    Tests support for extended ASCII characters.\n
    Returns True if its supported
    '''
    has_support = False

    # testing extended ascii compatibiliy for text table output
    try:
        print('CP437 charset support test '+slim_tbl_d.horiz, end=' ')
        print('OK')
        log.info('CP437 charset support OK')
        has_support = True
    except UnicodeEncodeError :
        print('FAILED')
        log.warning('CP437 charset not supported')
        has_support = False

    return has_support

def cprint(color: Color, *values: object, sep=' ', end: str = '\n'):
    '''
    Prints text similarly to `print()`, but with a specific color.\n
    `end` and `sep` are not colored.
    '''
    print(color.code_start, sep='', end='')
    print(*values, sep=sep, end='')
    print(color.code_end, sep='', end=end)

def get_date_text(
        date_format='{y}-{m}-{d}', 
        time_format='{h}-{m}-{s}',
        separator='_') -> str:
    '''
    Return the current date and time in a format that can be
    used for a file name.\n
    Accepted variables names:
    ```
    date_format:
        y: year
        m: month
        d: day
    time_format:
        h: hours
        m: minutes
        s: seconds
    ```
    '''
    current_datetime = datetime.datetime.now()
    date = '{y}-{m}-{d}'.format(
        d=str(current_datetime.day).zfill(2),
        m=str(current_datetime.month).zfill(2),
        y=str(current_datetime.year))   
    time = '{h}-{m}-{s}'.format(
        h=str(current_datetime.hour).zfill(2),
        m=str(current_datetime.minute).zfill(2),
        s=str(current_datetime.second).zfill(2))
    
    return date+separator+time
