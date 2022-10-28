"""
augment.py
-------------
Functions to apply augmentation method in mesh object.
"""

import numpy as np
import trimesh
import alphashape
import math
import time
import os
import glob
import collections
import pymeshfix



###############################
# Fix the mesh non watertight #
###############################
def fixNonWatertight(mesh):
    """
        This function fix the non watertight mesh to watertight mesh by pymeshfix lib
        and convert to trimesh. It will return mesh if that mesh had watertight and False
        if it didnt watertight.

        Parameters
        -----------
        mesh : trimesh.Trimesh

        Returns
        ------------
        mesh : trimesh.Trimesh or (False) Bool
    """

    meshfix = pymeshfix.MeshFix(
        mesh.vertices,
        mesh.faces
    )

    meshfix.repair()

    finalmesh = trimesh.Trimesh(meshfix.v, meshfix.f)

    if finalmesh.is_watertight == True:
        return finalmesh

    return False


############################
# Increasing mesh vertices #
############################
def take_first(elem):
    """
        take_first
    """
    return elem[0]


def makeMidPoints(lst_max_Face, _lst_vers, _lst_faces, lst_faces_needed_remove, list_index_face_Vertices):
    """
        makeMidPoints
    """

    for max_Face in lst_max_Face:
        if max_Face in lst_faces_needed_remove:
            continue
        lst_midpoint = []
        lst_vers = []
        # biến này chứa nội dung Face cần chia nhỏ có dạng [v1,v2,v3]
        content_Face = _lst_faces[max_Face]
        # biến này chứa vị trí của Face cần chia đang nằm ở đâu trong danh sách Faces, nó là phần tử thứ 1, nhớ là phần tử thứ 0 chính là diện tích
        index_Face = max_Face
        # đọc xem v1 ở vị trí thứ bao nhiêu gán vào biến index_v1
        index_v1 = content_Face[0]
        lst_vers.append(index_v1)
        # truy cập vào vị trí đó lấy ra tọa độ của v1, nhớ chú ý là khi truy cập vào list Vertices luôn phải trừ 1 như đã nói ở trên
        v1 = _lst_vers[index_v1]
        # tương tự cho 2 đỉnh còn lại
        index_v2 = content_Face[1]
        lst_vers.append(index_v2)
        v2 = _lst_vers[index_v2]
        index_v3 = content_Face[2]
        lst_vers.append(index_v3)
        v3 = _lst_vers[index_v3]

        lst_faces_needed_remove.append(index_Face)
        # lúc này v1 v2 v3 sẽ là tọa độ của 3 đỉnh tạo nên Face cần chia nhỏ, có dạng [x,y,z] là tọa độ của nó trong không gian
        # tính trung điểm  bằng cách lấy tổng x của 2 đỉnh chia 2, tương tự cho y và z
        mid_v1v3 = [(v1[0] + v3[0])/2, (v1[1] + v3[1])/2, (v1[2] + v3[2])/2]

        mid_v1v2 = [(v1[0] + v2[0])/2, (v1[1] + v2[1])/2, (v1[2] + v2[2])/2]
        mid_v2v3 = [(v3[0] + v2[0])/2, (v3[1] + v2[1])/2, (v3[2] + v2[2])/2]

        # vậy là ta có 3 trung điểm, bây giờ xét xem trung điểm đó có trùng với đỉnh nào trong danh sách đỉnh hiện tại không
        # một biến cờ nhằm báo có nếu như có, ban đầu mặc định là không

        # nếu có thì đã sử lý trong for rồi, nếu không thì thêm trung điểm đó vào danh sách đỉnh
        _lst_vers.append(mid_v1v3)
        # lúc này vị trí của điểm mới thêm vào chính là chiều dài của danh sách đỉnh vì nó được thêm ở sau cùng
        index_mid_v1v3 = len(_lst_vers)-1
        lst_midpoint.append(index_mid_v1v3)

        list_index_face_Vertices.append([])

        # tương tự cho 2 trung điểm còn lại
        _lst_vers.append(mid_v1v2)
        index_mid_v1v2 = len(_lst_vers) - 1
        lst_midpoint.append(index_mid_v1v2)
        list_index_face_Vertices.append([])

        _lst_vers.append(mid_v2v3)
        index_mid_v2v3 = len(_lst_vers)-1
        lst_midpoint.append(index_mid_v2v3)
        list_index_face_Vertices.append([])

        # giờ là thêm 3 faces có chứa vừa trung điểm vừa v vào danh sách faces
        _lst_faces.append([index_mid_v1v3, index_v1, index_mid_v1v2])
        list_index_face_Vertices[index_mid_v1v2].append(len(_lst_faces)-1)

        list_index_face_Vertices[index_mid_v1v3].append(len(_lst_faces)-1)
        list_index_face_Vertices[index_v1].append(len(_lst_faces)-1)
        _lst_faces.append([index_mid_v2v3, index_mid_v1v2, index_v2])

        list_index_face_Vertices[index_mid_v1v2].append(len(_lst_faces)-1)
        list_index_face_Vertices[index_mid_v2v3].append(len(_lst_faces)-1)
        list_index_face_Vertices[index_v2].append(len(_lst_faces)-1)

        _lst_faces.append([index_mid_v1v3, index_mid_v2v3, index_v3])

        list_index_face_Vertices[index_mid_v1v3].append(len(_lst_faces)-1)
        list_index_face_Vertices[index_mid_v2v3].append(len(_lst_faces)-1)
        list_index_face_Vertices[index_v3].append(len(_lst_faces)-1)
        # và face cuối hoàn toàn là do 3 trung điểm tạo thành
        _lst_faces.append([index_mid_v1v2, index_mid_v2v3, index_mid_v1v3])

        list_index_face_Vertices[index_mid_v1v2].append(len(_lst_faces)-1)
        list_index_face_Vertices[index_mid_v1v3].append(len(_lst_faces)-1)
        list_index_face_Vertices[index_mid_v2v3].append(len(_lst_faces)-1)

        list_index_face_Vertices[index_v1].remove(index_Face)
        list_index_face_Vertices[index_v2].remove(index_Face)
        list_index_face_Vertices[index_v3].remove(index_Face)

        for _idxmid in range(-1, 2):
            index_v1 = lst_vers[_idxmid]
            index_v2 = lst_vers[_idxmid+1]
            index_mid_v1v2 = lst_midpoint[_idxmid+1]
            _lst_facesv1v2 = []
            for _item in list_index_face_Vertices[index_v1]:
                _lst_facesv1v2.append(_item)
            for _item in list_index_face_Vertices[index_v2]:
                _lst_facesv1v2.append(_item)

            _faceremove = [k for k, v in collections.Counter(
                _lst_facesv1v2).items() if v > 1]

            if len(_faceremove) > 0:

                list_index_face_Vertices[_lst_faces[_faceremove[0]][0]].remove(
                    _faceremove[0])

                list_index_face_Vertices[_lst_faces[_faceremove[0]][1]].remove(
                    _faceremove[0])

                list_index_face_Vertices[_lst_faces[_faceremove[0]][2]].remove(
                    _faceremove[0])

                for _indx in _lst_faces[_faceremove[0]]:
                    if _indx != index_v1 and _indx != index_v2:
                        _other_ver = _indx

                lst_faces_needed_remove.append(_faceremove[0])
                _lst_faces.append([index_mid_v1v2, index_v1, _other_ver])
                list_index_face_Vertices[index_v1].append(len(_lst_faces)-1)
                list_index_face_Vertices[index_mid_v1v2].append(
                    len(_lst_faces)-1)
                list_index_face_Vertices[_other_ver].append(len(_lst_faces)-1)

                _lst_faces.append([index_mid_v1v2, _other_ver, index_v2])
                list_index_face_Vertices[index_v2].append(len(_lst_faces)-1)
                list_index_face_Vertices[index_mid_v1v2].append(
                    len(_lst_faces)-1)
                list_index_face_Vertices[_other_ver].append(len(_lst_faces)-1)

    # trả về danh sách Vertcies đã thêm 3 trung điểm và danh sách Faces đã thêm 4 faces nhỏ
    return _lst_vers, _lst_faces


def makeMidPoint(max_Face, _lst_vers, _lst_faces, lst_faces_needed_remove, list_index_face_Vertices):
    """
        makeMidPoint
    """
    if max_Face in lst_faces_needed_remove:
        return
    lst_midpoint = []
    lst_vers = []
    # biến này chứa nội dung Face cần chia nhỏ có dạng [v1,v2,v3]
    content_Face = _lst_faces[max_Face]
    # biến này chứa vị trí của Face cần chia đang nằm ở đâu trong danh sách Faces, nó là phần tử thứ 1, nhớ là phần tử thứ 0 chính là diện tích
    index_Face = max_Face
    # đọc xem v1 ở vị trí thứ bao nhiêu gán vào biến index_v1
    index_v1 = content_Face[0]
    lst_vers.append(index_v1)
    # truy cập vào vị trí đó lấy ra tọa độ của v1, nhớ chú ý là khi truy cập vào list Vertices luôn phải trừ 1 như đã nói ở trên
    v1 = _lst_vers[index_v1]

    index_v2 = content_Face[1]
    lst_vers.append(index_v2)
    v2 = _lst_vers[index_v2]
    index_v3 = content_Face[2]
    lst_vers.append(index_v3)
    v3 = _lst_vers[index_v3]

    # lúc này v1 v2 v3 sẽ là tọa độ của 3 đỉnh tạo nên Face cần chia nhỏ, có dạng [x,y,z] là tọa độ của nó trong không gian
    # tính trung điểm  bằng cách lấy tổng x của 2 đỉnh chia 2, tương tự cho y và z

    mid_v1v2 = [(v1[0] + v2[0])/2, (v1[1] + v2[1])/2, (v1[2] + v2[2])/2]
    _lst_vers.append(mid_v1v2)
    index_mid_v1v2 = len(_lst_vers) - 1
    lst_midpoint.append(index_mid_v1v2)
    list_index_face_Vertices.append([])

    index_v1 = lst_vers[0]
    index_v2 = lst_vers[1]
    index_mid_v1v2 = lst_midpoint[0]
    _lst_facesv1v2 = []
    for _item in list_index_face_Vertices[index_v1]:
        _lst_facesv1v2.append(_item)
    for _item in list_index_face_Vertices[index_v2]:
        _lst_facesv1v2.append(_item)

    _faceremove = [k for k, v in collections.Counter(
        _lst_facesv1v2).items() if v > 1]

    for fri in range(len(_faceremove)):

        list_index_face_Vertices[_lst_faces[_faceremove[fri]][0]].remove(
            _faceremove[fri])

        list_index_face_Vertices[_lst_faces[_faceremove[fri]][1]].remove(
            _faceremove[fri])

        list_index_face_Vertices[_lst_faces[_faceremove[fri]][2]].remove(
            _faceremove[fri])

        for _indx in _lst_faces[_faceremove[fri]]:
            if _indx != index_v1 and _indx != index_v2:
                _other_ver = _indx

        lst_faces_needed_remove.append(_faceremove[fri])
        _lst_faces.append([index_mid_v1v2, index_v1, _other_ver])
        list_index_face_Vertices[index_v1].append(len(_lst_faces)-1)
        list_index_face_Vertices[index_mid_v1v2].append(len(_lst_faces)-1)
        list_index_face_Vertices[_other_ver].append(len(_lst_faces)-1)

        _lst_faces.append([index_mid_v1v2, _other_ver, index_v2])
        list_index_face_Vertices[index_v2].append(len(_lst_faces)-1)
        list_index_face_Vertices[index_mid_v1v2].append(len(_lst_faces)-1)
        list_index_face_Vertices[_other_ver].append(len(_lst_faces)-1)

    # trả về danh sách Vertcies đã thêm 3 trung điểm và danh sách Faces đã thêm 4 faces nhỏ
    return _lst_vers, _lst_faces


def func_increase(_mesh, n,m, lst_faces_needed_remove,list_index_face_Vertices):
    """
        func_increase
    """
    tempmesh = _mesh.copy()
    list_vertice = tempmesh.vertices


    list_face = []
    list_area_faces = tempmesh.area_faces
    
    
    for i in range(len(tempmesh.faces)):
        # if func_checkZ(tempmesh.faces[i]):
        if i in lst_faces_needed_remove: continue
        list_face.append([list_area_faces[i], i])

    
    sorted_list_face = sorted(list_face, reverse=True, key=take_first)  
    max_area_divice = sorted_list_face[0][0]/4
    temp_lst_face = []
    for i in range( n ):
        
        if sorted_list_face[i][0] < max_area_divice: break
        temp_lst_face.append(sorted_list_face[i][1])
    vertices_sub_mesh = list(tempmesh.vertices)
    faces_sub_mesh    = list(tempmesh.faces)
    if m == 0:
        # vertices_sub_mesh, faces_sub_mesh = makeMidPoints(temp_lst_face,vertices_sub_mesh,faces_sub_mesh)
        vertices_sub_mesh, faces_sub_mesh = makeMidPoints(temp_lst_face,vertices_sub_mesh,faces_sub_mesh,lst_faces_needed_remove,list_index_face_Vertices)
    else:
        temp_lst_face_obo = []
        for i in range( m ):
            temp_lst_face_obo.append(sorted_list_face[i][1])
        for mfi in temp_lst_face_obo:
            vertices_sub_mesh, faces_sub_mesh = makeMidPoint(mfi,vertices_sub_mesh,faces_sub_mesh,lst_faces_needed_remove,list_index_face_Vertices)
    
    tempmesh = trimesh.Trimesh(vertices = vertices_sub_mesh, faces = faces_sub_mesh)

    return tempmesh


def generalMeshVertexIncreasing(original_mesh, max_point, step=200, debug=False):
    """
        generalMeshVertexIncreasing
    """
    mesh_increase = original_mesh.copy()
    # số điểm cần tăng
    max_point = max_point
    # số tam giác sẽ tăng mỗi lần lặp
    inc_p_l = step
    for _ in range(10000):
        if max_point - len(mesh_increase.vertices) <  inc_p_l*6 : 
            inc_p_l= int((max_point - len(mesh_increase.vertices))/3)
        if inc_p_l <1: 
            break
        if len(mesh_increase.vertices) > max_point: break
        list_index_face_Vertices = []
        for i in range ( len (mesh_increase.vertices )):
            list_index_face_Vertices.append( [] )
        for i in range( len( mesh_increase.faces ) ):
            list_index_face_Vertices[mesh_increase.faces[i][0]].append(i)
            list_index_face_Vertices[mesh_increase.faces[i][1]].append(i)
            list_index_face_Vertices[mesh_increase.faces[i][2]].append(i)
        lst_faces_needed_remove = []
        
        mesh_increase = func_increase(
            mesh_increase,
            inc_p_l,
            0,
            lst_faces_needed_remove,
            list_index_face_Vertices
            )

        full_faces = list(range(0, len(mesh_increase.faces)))
        lst_faces_needed_remove.sort(reverse=True)
        for _idx in lst_faces_needed_remove:
            full_faces.pop(_idx) 
        mesh_increase.update_faces(full_faces)
        if debug == True:
            print("Num Of vertices: ",print(len(mesh_increase.vertices)))
        
    if max_point - len(mesh_increase.vertices) > 0:

        list_index_face_Vertices = []
        for i in range ( len (mesh_increase.vertices )):
            list_index_face_Vertices.append( [] )
        for i in range( len( mesh_increase.faces ) ):
            list_index_face_Vertices[mesh_increase.faces[i][0]].append(i)
            list_index_face_Vertices[mesh_increase.faces[i][1]].append(i)
            list_index_face_Vertices[mesh_increase.faces[i][2]].append(i)
        lst_faces_needed_remove = []
        
        mesh_increase = func_increase(
            mesh_increase,
            1,
            max_point - len(mesh_increase.vertices),
            lst_faces_needed_remove,
            list_index_face_Vertices
            )

        full_faces = list(range(0, len(mesh_increase.faces)))
        lst_faces_needed_remove.sort(reverse=True)
        for _idx in lst_faces_needed_remove:
            full_faces.pop(_idx) 
        mesh_increase.update_faces(full_faces)
        if debug == True:
            print("Num Of vertices: ",len(mesh_increase.vertices))

    return mesh_increase



#################
# Scar Creating #
#################
def func_RandomFaces(_list_face):
    """
        func_RandomFaces
    """

    _index_Face = np.random.choice(_list_face)
    return _index_Face

def func_EyeSpace(_vertices):
    """
        func_EyeSpace
    """

    listY = []
    for i in range(0, len(_vertices)):
        listY.append(_vertices[i][1])
    
    minY = min(listY)
    maxY = max(listY)
    midY = (maxY - minY) / 10
    limitY_min = midY * 6
    limitY_max = midY * 7
    return (limitY_min, limitY_max)

def func_checkZ(_vertices,_face):
    """
        func_checkZ
    """
    _Z_vertice0_face = _vertices[_face[0]][2]
    _Z_vertice1_face = _vertices[_face[1]][2]
    _Z_vertice2_face = _vertices[_face[2]][2]
    
    if _Z_vertice0_face > 0 and _Z_vertice1_face > 0 and _Z_vertice2_face > 0:
        return True
    else:
        return False

#hàm kiểm tra Z Vertice của face
def func_checkY(_vertices,_face, _limitY_min, _limitY_max):
    """
        func_checkY
    """
    _Y_vertice0_face = _vertices[_face[0]][1]
    _Y_vertice1_face = _vertices[_face[1]][1]
    _Y_vertice2_face = _vertices[_face[2]][1]
    if _Y_vertice0_face < _limitY_min and _Y_vertice1_face < _limitY_min and _Y_vertice2_face < _limitY_min:
      return True
    elif _Y_vertice0_face > _limitY_max and _Y_vertice1_face > _limitY_max and _Y_vertice2_face > _limitY_max:
      return True
    else:
      return False

# danh sách Vertice cần tìm
# ngẫu nhiên => lan tràn ra và thường có hình tròn
# return List Index Vertice
def func_SpreadVertices(_mesh, _number_end, _face_start, list_face_of_vertice):
    """
        func_SpreadVertices
    """
    #face random
    _face_end = []

    #danh sách Vertice sau khi lấy
    _list_vertices = []
    _list_vertices.append(_face_start[0])
    _list_vertices.append(_face_start[1])
    _list_vertices.append(_face_start[2])
    m = 0
    next_len_list_vertices = 0

    #dừng khi số lượng Vertice lớn hơn số lượng cần tìm
    while len(_list_vertices) < _number_end:
        pre_len_list_vertices = len(_list_vertices)
        n = len(_list_vertices)
        #tăng dần
        for i in range(m, n):
            _neighbors_vertices = _mesh.vertex_neighbors[_list_vertices[i]]
            _list_vertices.extend(_neighbors_vertices)
            _list_vertices = list(dict.fromkeys(_list_vertices))

        m = n
        next_len_list_vertices = len(_list_vertices)
        if pre_len_list_vertices == next_len_list_vertices:
            break
    
    _end_vertice = _list_vertices[-1]
    temp_list_face_of_vertice = list_face_of_vertice[_end_vertice]

    for i in range(0, len(temp_list_face_of_vertice)):
        if func_checkZ(_mesh.vertices,_mesh.faces[temp_list_face_of_vertice[i]]):
            _face_end = _mesh.faces[temp_list_face_of_vertice[i]]
            break

    return (_list_vertices, _face_end)

def func_Vertice(_face, _vertice_0, _vertice_1):
    """
        func_Vertice
    """
    _index_Vertice_0 = -1
    _index_Vertice_1 = -1
    
    for i in range(0,len(_face)):
        if(_vertice_0 == _face[i]):
            _index_Vertice_0 = _face[i]
            break
    
    for i in range(0,len(_face)):
        if(_vertice_1 == _face[i]):
            _index_Vertice_1 = _face[i]
            break
            
    if (_index_Vertice_0 == -1 or _index_Vertice_1 == -1):
        return -1
    else:
        for i  in range(0,len(_face)):
            if(_face[i] != _index_Vertice_0 and _face[i] != _index_Vertice_1):
                return _face[i]

# danh sách Vertices cần tìm
# theo đường thằng duyệt từ đầu danh sách cặp cạnh với bước nhảy là  1
# return List Index Vertice
def func_LineVertices(_mesh,_number_end, _face_start, list_face_of_vertice):
    """
        func_LineVertices
    """

    #danh sách Vertice sau khi lấy
    _list_Vertices = []
    _face_end = []
    try:
        _list_Vertices.append(_face_start[0])
        _list_Vertices.append(_face_start[1])
        _list_Vertices.append(_face_start[2])
    except:
        _face_end = _face_start
        return (_list_Vertices, _face_end)


    #danh sách các cặp cạnh được tạo
    _list_Edges = []
    _list_Edges.append([_list_Vertices[0], _list_Vertices[1]])
    _list_Edges.append([_list_Vertices[0], _list_Vertices[2]])
    _list_Edges.append([_list_Vertices[1], _list_Vertices[2]])
    
    #danh sách để duyệt ngẫu nhiên các cặp cạnh
    _list_k = []
    next_len_list_vertices = 0
    #dừng khi số lượng Vertice lớn hơn số lượng cần tìm
    while (len(_list_Vertices) < _number_end):
        pre_len_list_vertices = len(_list_Vertices)
        n = len(_list_Edges)
        for k in range(0, n):
            if k not in _list_k:
                #thêm k vào danh sách
                _list_k.append(k)
                
                _list_face_temp = []
                
                temp_list_face_of_vertice1 = list_face_of_vertice[_list_Edges[k][0]]
                _list_face_temp.extend(temp_list_face_of_vertice1)
                
                temp_list_face_of_vertice2 = list_face_of_vertice[_list_Edges[k][1]]
                _list_face_temp.extend(temp_list_face_of_vertice2)
                
                _list_face_temp = list(dict.fromkeys(_list_face_temp))

                #duyệt qua 
                for j in _list_face_temp:
                    try:
                        #so sánh vị trí vertice của face với cặp cạnh
                        _result = func_Vertice(_mesh.faces[j], _list_Edges[k][0], _list_Edges[k][1])
                        #nếu kết quả trả về != 1 thì thêm vào danh sách
                        #và dừng vòng lặp
                        if _result != -1:
                            if _result not in _list_Vertices:
                                _list_Vertices.append(_result)
                                _face_end = _mesh.faces[j]
                                _list_Edges.append([_list_Edges[k][0], _result])
                                _list_Edges.append([_list_Edges[k][1], _result])
                                break
                    except:
                        print("Oops! Systems occurred.")

        next_len_list_vertices = len(_list_Vertices)
        if pre_len_list_vertices == next_len_list_vertices:
            break
    return (_list_Vertices, _face_end)

def func_MixVertices(mesh, list_index_face, list_face_of_vertice):
    """
        func_MixVertices
    """

    #face random
    _face = mesh.faces[ func_RandomFaces(list_index_face)]

    #số lượng Vertice sẽ lấy
    _number_vertice =  np.random.randint(1000, 5000)

    #danh sách để duyệt ngẫu nhiên các cặp cạnh
    _list_vertice = []
    _number = int(_number_vertice / 5)
    _face_start = _face
    #dừng khi số lượng Vertice lớn hơn số lượng cần tìm
    for i in range(0, 5):
        if i%2 == 0:
            _end_number = _number * (i + 1)
            temp_list_vertice, _temp_face_start = func_SpreadVertices(mesh, _end_number, _face_start, list_face_of_vertice)
            if any(_temp_face_start):
                _face_start = _temp_face_start

            _list_vertice.extend(temp_list_vertice)
            _list_vertice = list(dict.fromkeys(_list_vertice))
        else:
            _end_number = _number * (i + 1)
            temp_list_vertice, _temp_face_start = func_LineVertices(mesh, _end_number, _face_start, list_face_of_vertice)
            if any(_temp_face_start):
                _face_start = _temp_face_start
            _list_vertice.extend(temp_list_vertice)
            _list_vertice = list(dict.fromkeys(_list_vertice))
                        
    return _list_vertice

def func_SaveFile(_mesh, _list_boundary, _new_obj_path, _inorde):
    """
        func_SaveFile
    """

    new_mesh = _mesh.copy()

    #giá trị để biết là tăng hay giảm Z
    #-1 giảm
    #!= -1 tăng
    # if _inorde != -1 and _inorde != 1:
    # _inorde = np.random.randint(0,2) * 2 - 1
    
    #giá trị biến động của Z
    _deep = np.random.uniform(4, 10)
    if (_inorde != 1):
        _deep = -_deep

    
    z = _deep/len(_list_boundary)
    
    for i in range(0, len(_list_boundary)):
        for index_vertice in _list_boundary[i]:
            new_mesh.vertices[index_vertice][2] = new_mesh.vertices[index_vertice][2] + (z * i)

    new_mesh.export(_new_obj_path)
    print(new_mesh.is_watertight)

def func_ListBoundary(_mesh, _list_Vertices):
    """
        func_ListBoundary
    """

    list_boundary = []
    list_find_Vertices_copy = _list_Vertices.copy()
    # stop_find_boundary = (0.95*len(_list_Vertices))
    count = 0
    for k in range(0, 1000):
        
        # if count > stop_find_boundary:
        #     break

        m = len(list_find_Vertices_copy)
        if m < 5:
            break
        
        listxy = []
        for i in range(0, len(list_find_Vertices_copy)):
            listxy.append([
                _mesh.vertices[list_find_Vertices_copy[i]][0], 
                _mesh.vertices[list_find_Vertices_copy[i]][1], 
                _mesh.vertices[list_find_Vertices_copy[i]][2]
            ])
        shape = alphashape.alphashape(listxy, 0)
        shape_x, shape_y = shape.exterior.coords.xy

        list_temp_boundary = []
        for i in range (0, len(list_find_Vertices_copy)):
            for j in range (0, len(shape_x)):
                if _mesh.vertices[list_find_Vertices_copy[i]][0] == shape_x[j] and _mesh.vertices[list_find_Vertices_copy[i]][1] == shape_y[j]:
                    list_temp_boundary.append(list_find_Vertices_copy[i])
                    count = count + 1
                    
        list_temp_boundary = list(dict.fromkeys(list_temp_boundary))
        list_boundary.append(list_temp_boundary)

        for i in range (0, len(list_temp_boundary)):
            for j in range (0, len(list_find_Vertices_copy)):
                if list_find_Vertices_copy[j] == list_temp_boundary[i]:
                    list_find_Vertices_copy.remove(list_find_Vertices_copy[j])
                    break
                    
    list_boundary.append(list_find_Vertices_copy)
    return list_boundary

def func_randomFuncOutMesh(_path, _directory, _mesh, list_index_face, list_face_of_vertice):
    """
        func_randomFuncOutMesh
    """

    for i in range(1, 11):
        #thời gian bắt đầu chạy
        # start = time.time()
        new_obj_path = _path + '/' + _directory + '_' + str(i) + '.obj'

        list_Vertices = func_MixVertices(_mesh, list_index_face, list_face_of_vertice)

        list_Boundary = func_ListBoundary(_mesh, list_Vertices)
        func_SaveFile(_mesh, list_Boundary, new_obj_path, 1)
        #thời gian kết thúc 1 file obj
        # end = time.time()
        # print(end - start, "seconds")
    
    for i in range(11, 21):
        #thời gian bắt đầu chạy
        # start = time.time()
        new_obj_path = _path + '/' + _directory + '_' + str(i) + '.obj'
        list_Vertices = func_MixVertices(_mesh, list_index_face, list_face_of_vertice)

        list_Boundary = func_ListBoundary(_mesh, list_Vertices)
        func_SaveFile(_mesh, list_Boundary, new_obj_path, -1)
        #thời gian kết thúc 1 file obj
        # end = time.time()
        # print(end - start, "seconds")

def func_ListFaceOfVertice(_mesh):
    """
        func_ListFaceOfVertice
    """

    _lstfv = []
    for i in range(0, len(_mesh.vertices)):
        _lstfv.append([])
        
    for i in range(0, len(_mesh.faces)):
        _lstfv[_mesh.faces[i][0]].append(i)
        _lstfv[_mesh.faces[i][1]].append(i)
        _lstfv[_mesh.faces[i][2]].append(i)
    return _lstfv

def scarCreating(mesh, path, directory):
    """
        scarCreating
    """
    trimesh.smoothing.filter_laplacian(mesh,0.8,3)
    list_face_of_vertice = func_ListFaceOfVertice(mesh)
    limitY_min, limitY_max = func_EyeSpace(mesh.vertices)
    list_index_face = []
    for i in range(0, len(mesh.faces)):
        if func_checkZ(mesh.vertices,mesh.faces[i]):
            if func_checkY(mesh.vertices,mesh.faces[i], limitY_min, limitY_max):
                list_index_face.append(i)

    func_randomFuncOutMesh(path, directory, mesh, list_index_face, list_face_of_vertice)

    return True
    
