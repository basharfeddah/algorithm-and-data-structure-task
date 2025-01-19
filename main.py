from collections import defaultdict, deque


class Graph:
    def __init__(self, vertices):
        self.V = vertices  # عدد الرؤوس
        self.adj = defaultdict(list)  # قائمة المجاورات

    def add_edge(self, u, v):
        """إضافة حافة بين الرأس u والرأس v"""
        self.adj[u].append(v)

    def dfs(self, v, visited):
        """تنفيذ البحث بالعمق (DFS)"""
        visited[v] = True
        for neighbor in self.adj[v]:
            if not visited[neighbor]:
                self.dfs(neighbor, visited)

    def is_strongly_connected(self):
        """التحقق مما إذا كان البيان متصلًا بقوة"""
        # الخطوة 1: تحقق إذا كان جميع الرؤوس يمكن الوصول إليها من الرأس الأول
        visited = [False] * self.V
        self.dfs(0, visited)
        if not all(visited):
            return False

        # الخطوة 2: أنشئ البيان العكسي
        reversed_graph = self.get_transpose()

        # الخطوة 3: تحقق مرة أخرى باستخدام البيان العكسي
        visited = [False] * self.V
        reversed_graph.dfs(0, visited)
        return all(visited)

    def get_transpose(self):
        """إنشاء بيان عكسي"""
        reversed_graph = Graph(self.V)
        for u in self.adj:
            for v in self.adj[u]:
                reversed_graph.add_edge(v, u)
        return reversed_graph

    def melhorn_algorithm(self):
        """تنفيذ خوارزمية Melhorn لتحسين الاتصال"""
        if self.is_strongly_connected():
            print("The graph is already strongly connected.")
            return

        # إضافة حواف لجعل البيان متصلًا بقوة
        # (بسيط للتوضيح، يجب تحسينه اعتمادًا على التطبيق العملي)
        for u in range(self.V):
            for v in range(self.V):
                if u != v and v not in self.adj[u]:
                    self.add_edge(u, v)
                    if self.is_strongly_connected():
                        print(f"Added edge ({u}, {v}) to make the graph strongly connected.")
                        return

    def is_2_edge_connected(self):
        """التحقق إذا كان البيان مضاعف الترابط من حيث الحواف"""
        discovery = [-1] * self.V
        low = [-1] * self.V
        parent = [-1] * self.V
        time = [0]  # وقت الاكتشاف أثناء الـ DFS

        def dfs_2_edge(v):
            discovery[v] = low[v] = time[0]
            time[0] += 1
            children = 0

            for neighbor in self.adj[v]:
                if discovery[neighbor] == -1:  # إذا لم تتم زيارته
                    parent[neighbor] = v
                    children += 1
                    dfs_2_edge(neighbor)
                    low[v] = min(low[v], low[neighbor])

                    # إذا كان هناك نقطة قطع (Bridge)
                    if parent[v] == -1 and children > 1:
                        return False
                    if parent[v] != -1 and low[neighbor] >= discovery[v]:
                        return False
                elif neighbor != parent[v]:
                    low[v] = min(low[v], discovery[neighbor])
            return True

        return dfs_2_edge(0) and all(d != -1 for d in discovery)

    def is_2_vertex_connected(self):
        """التحقق إذا كان البيان مضاعف الترابط من حيث الرؤوس"""
        discovery = [-1] * self.V
        low = [-1] * self.V
        parent = [-1] * self.V
        time = [0]

        def dfs_2_vertex(v):
            discovery[v] = low[v] = time[0]
            time[0] += 1
            children = 0

            for neighbor in self.adj[v]:
                if discovery[neighbor] == -1:  # إذا لم تتم زيارته
                    parent[neighbor] = v
                    children += 1
                    if not dfs_2_vertex(neighbor):
                        return False
                    low[v] = min(low[v], low[neighbor])

                    # إذا كان هناك نقطة قطع (Articulation Point)
                    if parent[v] == -1 and children > 1:
                        return False
                    if parent[v] != -1 and low[neighbor] >= discovery[v]:
                        return False
                elif neighbor != parent[v]:
                    low[v] = min(low[v], discovery[neighbor])
            return True

        return dfs_2_vertex(0) and all(d != -1 for d in discovery)


# ======== اختبار الكود ========

# إنشاء بيان موجه
g = Graph(5)
g.add_edge(0, 1)
g.add_edge(1, 2)
g.add_edge(2, 3)
g.add_edge(3, 0)
g.add_edge(2, 4)

print("DFS Example:")
visited = [False] * g.V
g.dfs(0, visited)
print("Visited:", visited)

print("\nIs Strongly Connected:", g.is_strongly_connected())

print("\nRunning Melhorn's Algorithm...")
g.melhorn_algorithm()

print("\nIs 2-Edge-Connected:", g.is_2_edge_connected())
print("Is 2-Vertex-Connected:", g.is_2_vertex_connected())
