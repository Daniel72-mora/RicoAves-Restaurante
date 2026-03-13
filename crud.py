import mysql.connector

def ejecutar_query(sql, valores=None, es_consulta=False):
    try:
        conn = mysql.connector.connect(
            host="localhost", user="root", password="", database="rico_aves"
        )
        cursor = conn.cursor()
        cursor.execute(sql, valores)
        
        if es_consulta:
            resultado = cursor.fetchall()
            return resultado
        
        conn.commit()
        return True
    except Exception as e:
        print(f"\n❌ Error de base de datos: {e}")
        return None
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# --- MENÚS DE LA INTERFAZ ---
def menu_principal():
    print("\n" + "="*40)
    print("   SISTEMA ADMINISTRATIVO RICO AVES")
    print("="*40)
    print("1. GESTIÓN DE PRODUCTOS")
    print("2. GESTIÓN DE CLIENTES")
    print("3. REGISTRAR VENTA (PEDIDO)")
    print("4. VER HISTORIAL DE VENTAS")
    print("5. SALIR")
    return input("Seleccione una opción: ")

# --- LÓGICA PRINCIPAL ---
while True:
    opcion = menu_principal()

    if opcion == "1":
        print("\n--- SUBMENÚ PRODUCTOS ---")
        print("a. Agregar | b. Ver Catálogo | c. Actualizar Precio | d. Eliminar")
        sub = input("Seleccione: ").lower()

        if sub == "a":
            nom = input("Nombre del plato: ")
            desc = input("Descripción: ")
            pre = float(input("Precio: "))
            cat = input("Categoría (Individual/Combo/Bebida): ")
            sql = "INSERT INTO productos (nombre, descripcion, precio, categoria) VALUES (%s, %s, %s, %s)"
            ejecutar_query(sql, (nom, desc, pre, cat))
            print("✅ Producto guardado.")

        elif sub == "b":
            res = ejecutar_query("SELECT * FROM productos", es_consulta=True)
            if res:
                print("\nID | NOMBRE | PRECIO | CATEGORÍA")
                for p in res: print(f"{p[0]} | {p[1]} | ${p[3]} | {p[4]}")
            else: print("No hay productos.")

        elif sub == "c":
            id_p = int(input("ID del producto: "))
            nuevo_p = float(input("Nuevo precio: "))
            ejecutar_query("UPDATE productos SET precio = %s WHERE id_producto = %s", (nuevo_p, id_p))
            print("✅ Precio actualizado.")

        elif sub == "d":
            id_p = int(input("ID del producto a borrar: "))
            ejecutar_query("DELETE FROM productos WHERE id_producto = %s", (id_p,))
            print("✅ Producto eliminado.")

    # 2. GESTIÓN DE CLIENTES (CORREGIDO)
    elif opcion == "2":
        print("\n--- REGISTRO DE CLIENTES ---")
        nom = input("Nombre completo: ")
        tel = input("Teléfono: ")
        direc = input("Dirección: ")
        mail = input("Correo: ")
        sql = "INSERT INTO clientes (nombre, telefono, direccion, email) VALUES (%s, %s, %s, %s)"
        ejecutar_query(sql, (nom, tel, direc, mail))
        print("✅ Cliente registrado correctamente.")

    # 3. REGISTRAR VENTA
    elif opcion == "3":
        print("\n--- NUEVA VENTA ---")
        clis = ejecutar_query("SELECT id_cliente, nombre FROM clientes", es_consulta=True)
        if clis:
            for c in clis: print(f"ID: {c[0]} - {c[1]}")
            try:
                id_c = int(input("\nID del Cliente: "))
                id_p = int(input("ID del Producto: "))
                cant = int(input("Cantidad: "))
                sql = "INSERT INTO pedidos (id_cliente, id_producto, cantidad) VALUES (%s, %s, %s)"
                ejecutar_query(sql, (id_c, id_p, cant))
                print("✅ ¡Venta registrada exitosamente!")
            except ValueError:
                print("⚠️ Error: Debe ingresar números válidos para ID y cantidad.")
        else: print("No hay clientes registrados.")

    # 4. HISTORIAL
    elif opcion == "4":
        sql = """
            SELECT p.id_pedido, c.nombre, pr.nombre, p.cantidad, (pr.precio * p.cantidad)
            FROM pedidos p
            JOIN clientes c ON p.id_cliente = c.id_cliente
            JOIN productos pr ON p.id_producto = pr.id_producto
        """
        ventas = ejecutar_query(sql, es_consulta=True)
        if ventas:
            for v in ventas:
                print(f"Ticket #{v[0]} | Cliente: {v[1]} | Producto: {v[2]} | Cant: {v[3]} | Total: ${v[4]}")
        else: print("No hay ventas registradas.")

    elif opcion == "5":
        print("Cerrando sistema. ¡Hasta pronto!")
        break
    else:
        print("⚠️ Opción no válida.")