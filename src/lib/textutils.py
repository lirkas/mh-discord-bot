import logging as log


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

# creates a text table and populates it with content
#       content : 2D matrix that hold each cell's value
#       column_sizes : array of int that defines each column max width
def text_table(content: list[list], row_height = 1, min_column_size = 0, column_sizes: list = None, 
               table_delimiters: TableSegments = default_tbl_d):
    
    log.info('creating text table')
    # positions for content's cells
    r = 0
    c = 0

    tbl_d = table_delimiters
    # if the encoding is not supported - use default
    try:
        print('test: '+tbl_d.bot_left)
    except UnicodeEncodeError :
        log.warning('charset for table delimiter not supported')
        log.warning('fallback to ascii default charset')
        tbl_d = default_tbl_d

    table_text = ''
    cell_text = ''

    row_blocks = len(content)
    column_blocks = len(content[0])

    # exact amount of 'characters rows'
    rows = (row_blocks * (1 + row_height)) + 1 

    # automatically defining the max width for each column
    # based on each cell content if the sizes are not provided
    if column_sizes == None:
        log.info('automatically defining columns sizes')
    
        column_sizes = [min_column_size] * column_blocks

        while r < row_blocks:

            while c < column_blocks:
                if column_sizes[c] < len(content[r][c]):
                    column_sizes[c] = len(content[r][c])
                
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