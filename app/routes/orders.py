from fastapi import APIRouter, HTTPException
from psycopg2.extras import RealDictCursor
from app.database import get_connection
from app.schemas import OrderCreate, OrderUpdate, OrderStatus

router = APIRouter(prefix="/orders", tags=["Orders"])

#CREATE ORDER
@router.post("/")
def create_order(order: OrderCreate):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cur.execute("""
            SELECT id, stock_quantity
            FROM products
            WHERE id = %s
        """, (order.product_id,))
        
        product = cur.fetchone()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        if product["stock_quantity"] < order.quantity:
            raise HTTPException(status_code=400, detail="Not enough stock available")

        cur.execute("""
            INSERT INTO orders (customer_name, product_id, quantity, status)
            VALUES (%s, %s, %s, %s)
            RETURNING id, customer_name, product_id, quantity, status, created_at
        """, (
            order.customer_name,
            order.product_id,
            order.quantity,
            order.status.value
        ))

        new_order = cur.fetchone()

        cur.execute("""
            UPDATE products
            SET stock_quantity = stock_quantity - %s
            WHERE id = %s
        """, (order.quantity, order.product_id))

        conn.commit()

        return {
            "message": "Order created successfully",
            "order": new_order
        }

    except HTTPException:
        conn.rollback()
        raise

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    finally:
        cur.close()
        conn.close()
#READ ALL ORDERS
@router.get("/")
def get_orders():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cur.execute("""
            SELECT id, customer_name, product_id, quantity, status, created_at
            FROM orders
            ORDER BY id DESC
    """)
        
        orders = cur.fetchall()
    
        
        return {
            "total_orders": len(orders),
            "orders":orders}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
 
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

#SEARCH ORDER

#READ ONE ORDER
@router.get("/{order_id}")
def get_order(order_id: int):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cur.execute("""
        SELECT id, customer_name, product_id, quantity, status, created_at
        FROM orders
        where id = %s
                    """, (order_id,))

        order = cur.fetchone()

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        return order

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    finally:
        cur.close()
        conn.close()
#UPDATE ORDER
@router.patch("/{order_id}/status")
def update_order_status(order_id: int, status: OrderStatus):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cur.execute("""
            SELECT id
            FROM orders
            WHERE id = %s
        """, (order_id,))
        existing_order = cur.fetchone()

        if not existing_order:
            raise HTTPException(status_code=404, detail="Order not found")

        cur.execute("""
            UPDATE orders
            SET status = %s
            WHERE id = %s
            RETURNING id, customer_name, product_id, quantity, status, created_at
        """, (status.value, order_id))
        updated_order = cur.fetchone()

        conn.commit()

        return {
            "message": "Order status updated successfully",
            "order": updated_order
        }

    except HTTPException:
        conn.rollback()
        raise

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    finally:
        cur.close()
        conn.close()

#DELETE ORDER
@router.delete("/{order_id}")
def delete_order(order_id: int):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("""
            SELECT id, product_id, quantity, status
            FROM orders
            WHERE id = %s
        """, (order_id,))
        order = cur.fetchone()

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        if order["status"] != "cancelled":
            cur.execute("""
                UPDATE products
                SET stock_quantity = stock_quantity + %s
                WHERE id = %s
            """, (order["quantity"], order["product_id"]))

        cur.execute("""
            DELETE FROM orders
            WHERE id = %s
        """, (order_id,))

        conn.commit()

        return {
            "message": "Order deleted successfully"
        }

    except HTTPException:
        conn.rollback()
        raise

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    finally:
        cur.close()
        conn.close()
        