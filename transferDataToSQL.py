import psycopg2

hostname = 'HOSTNAME'
username = 'USERNAME'
password = 'PASSWORD'
database = 'DATABASE'

myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )

data =  ''' Create Table problems
        (
            number int,
            name char(156),
            subscription bool,
            link char(156),
            acceptance float,
            difficulty char(32),
            Arrays boolean,
            Hash_Table boolean,
            Linked_Lists boolean,
            Math boolean,
            Two_Pointers boolean,
            String boolean,
            Binary_Search boolean,
            Divide_and_Conquer boolean,
            Dynamic_Programming boolean,
            Backtracking boolean,
            Stack boolean,
            Heap boolean,
            Greedy boolean,
            Sort boolean,
            Bit_Manipulation boolean,
            Tree boolean,
            Depth_First_Search boolean,
            Breadth_First_Search boolean,
            Union_Find boolean,
            Graph boolean,
            Design boolean,
            Topological_Sort boolean,
            Trie boolean,
            Binary_Indexed_Tree boolean,
            Segment_Tree boolean,
            Binary_Search_Tree boolean,
            Recursion boolean,
            Brain_Teaser boolean,
            Memoization boolean,
            Queue boolean,
            Minimax boolean,
            Reservoir_Sampling boolean,
            Ordered_Map boolean,
            Geometry boolean,
            Random boolean,
            Rejection_Sampling boolean,
            Sliding_Window boolean,
            Line_Sweep boolean,
            Rolling_Hash boolean,
            Suffix_Array boolean
        )
        '''
cursor = myConnection.cursor()

cursor.execute(data)

f = open('mergedLeetcodeData.csv', 'r')
cursor.copy_from(f , 'problems', sep=',')
f.close()


myConnection.commit()

myConnection.close()

